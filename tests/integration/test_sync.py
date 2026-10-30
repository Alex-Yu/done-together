from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from datetime import timezone as dtz
from threading import Event
from unittest.mock import patch

import pytest
from django.db import close_old_connections
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from chores.models import Approval
from chores.services import save_one_off
from households.models import BoardAuthority, Child, Household
from tests.integration.test_review import post_review, post_submit, ready


def snapshot(c, h, key=None):
    return c.get(reverse("board_snapshot", args=[h.pk]), {"key": key or ""})


@pytest.mark.django_db
def test_revision_poll_scope_no_secrets_and_passive_expiry():
    a, _, h, c, child, w = ready()
    before = BoardAuthority.objects.get().last_activity
    first = snapshot(c, h)
    assert first.status_code == 200
    data = first.json()
    assert w.title in data["columns"] and child.name in data["columns"]
    assert child.pin_hash not in first.content.decode()
    assert "no-store" in first["Cache-Control"]
    assert snapshot(c, h, data["key"]).json() == {"key": data["key"], "unlocked": True}
    assert BoardAuthority.objects.get().last_activity == before
    assert post_submit(c, h, w).status_code == 302
    after = snapshot(c, h, data["key"]).json()
    assert after["key"] != data["key"] and "Awaiting approval" in after["columns"]
    assert BoardAuthority.objects.get().last_activity == before
    BoardAuthority.objects.update(last_activity=timezone.now() - timedelta(seconds=60))
    locked = snapshot(c, h, after["key"]).json()
    assert not locked["unlocked"] and "Review chore" not in locked["columns"]
    assert snapshot(Client(), h).status_code == 403
    from allauth.account.models import EmailAddress
    from django.contrib.auth import get_user_model

    from households.services import create_household

    other = get_user_model().objects.create_user(
        username="foreign", email="foreign@example.test"
    )
    EmailAddress.objects.create(user=other, email=other.email, verified=True)
    oh = create_household(other, "UTC")
    Child.objects.create(household=oh, name="Foreign private child", pin_hash="secret")
    outsider = Client()
    outsider.force_login(other)
    assert snapshot(outsider, h).status_code == 403
    assert "Foreign private child" not in snapshot(c, h).content.decode()
    EmailAddress.objects.filter(user=a).update(verified=False)
    assert snapshot(c, h).status_code == 403


@pytest.mark.django_db
def test_week_marker_rolls_without_mutation_and_current_snapshot_totals():
    _, _, h, c, _, w = ready()
    assert post_submit(c, h, w).status_code == 302
    w.refresh_from_db()
    sunday = datetime(2026, 11, 1, 23, 59, 59, tzinfo=dtz.utc)
    # Household fixture UTC.
    Household.objects.filter(pk=h.pk).update(timezone="UTC")
    with patch("django.utils.timezone.now", return_value=sunday):
        # Refresh authority for synthetic future instant, no inactivity bypass.
        BoardAuthority.objects.update(last_activity=sunday)
        assert post_review(c, h, w).status_code == 302
        first = snapshot(c, h).json()
    h.refresh_from_db()
    rev = h.revision
    with patch("django.utils.timezone.now", return_value=sunday + timedelta(seconds=1)):
        second = snapshot(c, h, first["key"]).json()
    assert first["key"] != second["key"]
    assert "This week: 1 star" in first["columns"]
    assert (
        "This week: 0 stars" in second["columns"]
        and "All time: 1 star" in second["columns"]
    )
    assert w.title not in second["columns"]
    h.refresh_from_db()
    assert h.revision == rev and Approval.objects.count() == 1


@pytest.mark.django_db
def test_child_edit_conflict_and_atomic_revision_increment():
    _, _, h, c, child, _ = ready()
    url = reverse("child_edit", args=[h.pk, child.pk])
    revision = c.get(url).context["form"].initial["revision"]
    assert (
        c.post(url, {"name": "First accepted", "revision": revision}).status_code == 302
    )
    result = c.post(url, {"name": "Stale rejected", "revision": revision})
    assert result.status_code == 400 and b"This household changed" in result.content
    child.refresh_from_db()
    assert child.name == "First accepted"
    h.refresh_from_db()
    assert h.revision == revision + 1
    assert c.post(url, {"name": "Missing version"}).status_code == 400


@pytest.mark.django_db(transaction=True)
def test_snapshot_serializes_revision_with_actual_content(monkeypatch):
    _, _, h, c, child, _ = ready()
    entered = Event()
    release = Event()
    from board import sync

    original = sync.columns_for_household

    def pause(household):
        entered.set()
        assert release.wait(5)
        return original(household)

    monkeypatch.setattr(sync, "columns_for_household", pause)

    def read():
        close_old_connections()
        try:
            return snapshot(c, h).json()
        finally:
            close_old_connections()

    def write():
        close_old_connections()
        try:
            return save_one_off(
                h,
                {
                    "title": "Concurrent after snapshot",
                    "child": child,
                    "due_date": timezone.now().date(),
                },
            )
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as pool:
        future = pool.submit(read)
        assert entered.wait(5)
        writer = pool.submit(write)
        assert not writer.done()
        release.set()
        first = future.result()
        writer.result()
    monkeypatch.setattr(sync, "columns_for_household", original)
    second = snapshot(c, h, first["key"]).json()
    assert "Concurrent after snapshot" not in first["columns"]
    assert (
        "Concurrent after snapshot" in second["columns"]
        and first["key"] != second["key"]
    )
