from datetime import date, timedelta
from unittest.mock import patch

import pytest
from django.db import OperationalError
from django.test import Client, override_settings
from django.urls import reverse
from django.utils import timezone

from board.read_model import Card, State, VisibleWork
from households.models import BoardAuthority, Child
from tests.integration.test_pins import fixture, setup, unlock


def mixed_work(child_id):
    today = date.today()
    return {
        child_id: VisibleWork(
            (
                Card(
                    "todo",
                    "Water the extraordinarily long windowsill plants",
                    State.TO_DO,
                    today,
                ),
                Card(
                    "late",
                    "Old active assignment",
                    State.TO_DO,
                    today - timedelta(days=20),
                    True,
                ),
                Card("review", "Awaiting review", State.AWAITING, today),
            ),
            (
                Card(
                    "done",
                    "Current week approval",
                    State.COMPLETED,
                    today,
                    completed_at=timezone.now(),
                ),
            ),
        )
    }


@pytest.mark.django_db
def test_real_columns_empty_guidance_entry_and_household_isolation():
    a, _, h, client = fixture()
    url = reverse("household_board", args=[h.pk])
    assert client.get("/").url == url
    assert "Add children in household settings" in client.get(url).content.decode()
    child = Child.objects.create(household=h, name="Aster", pin_hash="private-hash")
    body = client.get(url + "?fixture=mixed").content.decode()
    assert "Aster" in body and "Nothing assigned yet." in body
    assert "private-hash" not in body and "Current week approval" not in body
    outsider = Client()
    # A second actual household, not a forged household ID.
    from allauth.account.models import EmailAddress
    from django.contrib.auth import get_user_model

    from households.services import create_household

    user = get_user_model().objects.create_user(
        username="other", email="other@example.test"
    )
    EmailAddress.objects.create(user=user, email=user.email, verified=True)
    other = create_household(user, "UTC")
    Child.objects.create(
        household=other, name="Foreign child", pin_hash="private-other"
    )
    outsider.force_login(user)
    assert outsider.get(url).status_code == 403
    assert "Foreign child" not in client.get(url).content.decode()
    assert (
        client.post(
            reverse("child_edit", args=[h.pk, child.pk]), {"name": "Denied"}
        ).status_code
        == 403
    )
    child.refresh_from_db()
    assert child.name == "Aster"


@pytest.mark.django_db
def test_internal_projection_visible_states_correct_columns_and_invalid_unlock():
    a, _, h, client = fixture()
    child = Child.objects.create(household=h, name="Aster", pin_hash="unused")
    Child.objects.create(household=h, name="Birch", pin_hash="unused")
    with patch("board.read_model.load_visible_work", return_value=mixed_work(child.pk)):
        response = client.get(reverse("household_board", args=[h.pk]))
        columns = response.context["columns"]
        assert [c.name for c in columns] == ["Aster", "Birch"]
        assert len(columns[0].work.items) == 4 and not columns[1].work.items
        body = response.content.decode()
        for text in [
            "To do",
            "Overdue",
            "Awaiting approval",
            "Completed",
            "Current week approval",
            "Old active assignment",
        ]:
            assert text in body
        assert "<details" not in body and 'data-work-id="done"' in body
        bad = client.post(
            reverse("parent_unlock", args=[h.pk]), {"parent": a.pk, "pin": "bad"}
        )
        assert (
            bad.status_code == 400 and "Current week approval" in bad.content.decode()
        )


@pytest.mark.django_db
def test_board_reads_do_not_refresh_parent_authority_and_expiry_keeps_columns():
    a, _, h, client = fixture()
    Child.objects.create(household=h, name="Still visible", pin_hash="unused")
    setup(client, h, a)
    unlock(client, h, a)
    authority = BoardAuthority.objects.get()
    before = authority.last_activity
    client.get(reverse("household_board", args=[h.pk]))
    authority.refresh_from_db()
    assert authority.last_activity == before
    BoardAuthority.objects.filter(pk=authority.pk).update(
        last_activity=timezone.now() - timedelta(seconds=61)
    )
    body = client.get(reverse("household_board", args=[h.pk])).content.decode()
    assert "Still visible" in body and "Parent controls locked." in body
    assert client.get(reverse("household_settings", args=[h.pk])).url == reverse(
        "household_board", args=[h.pk]
    )


@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_projection_database_failure_private_recoverable_and_retry(caplog):
    _, _, h, client = fixture()
    Child.objects.create(household=h, name="Stored", pin_hash="unused")
    url = reverse("household_board", args=[h.pk])
    with patch(
        "board.read_model.load_visible_work",
        side_effect=OperationalError("PRIVATE-BOARD-FAULT"),
    ):
        result = client.get(url)
    assert result.status_code == 503
    assert "PRIVATE-BOARD-FAULT" not in result.content.decode() + caplog.text
    assert Child.objects.filter(household=h, name="Stored").count() == 1
    assert client.get(url).status_code == 200


@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_entry_failure_is_generic_and_unverified_or_anonymous_cannot_read(caplog):
    a, _, h, client = fixture()
    with patch(
        "households.models.Membership.objects.filter",
        side_effect=OperationalError("PRIVATE-ENTRY-FAULT"),
    ):
        result = client.get("/")
    assert result.status_code == 503
    assert "PRIVATE-ENTRY-FAULT" not in result.content.decode() + caplog.text
    assert client.get("/").status_code == 302
    url = reverse("household_board", args=[h.pk])
    assert Client().get(url).status_code == 403
    from allauth.account.models import EmailAddress

    EmailAddress.objects.filter(user=a).update(verified=False)
    assert client.get(url).status_code == 403
    assert client.get("/").status_code == 200
