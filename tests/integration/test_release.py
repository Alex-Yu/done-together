"""Release-only HTTP integration of recurrence, review, snapshots and retention.

The synthetic bootstrap establishes verified members/one child. Every chore,
edit, submission, review and deletion below crosses actual product HTTP views.
"""

from datetime import date, datetime, timezone

import pytest
from django.core.management import call_command
from django.urls import reverse

from chores.models import Approval, Definition, Occurrence
from households.models import BoardAuthority, Child
from tests.integration.test_review import post_review, post_submit, ready


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    "initial_schedule,approval_day,expected_day",
    [("daily", 28, 28), ("weekdays", 28, 28), ("weekdays", 27, None)],
)
def test_http_release_recurrence_late_approval_future_edit_and_retention(
    monkeypatch, initial_schedule, approval_day, expected_day
):
    _, _, household, client, child, _ = ready()
    instant = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)  # Monday
    monkeypatch.setattr("django.utils.timezone.now", lambda: instant)

    def authorize():
        # Clock movement is scenario setup; real authority was granted through
        # the existing HTTP setup fixture. Never bypass role/state decisions.
        BoardAuthority.objects.update(last_activity=instant)

    authorize()
    assert (
        client.post(
            reverse("child_create", args=[household.pk]),
            {"name": "Birch release", "pin": "0123"},
        ).status_code
        == 302
    )
    other = Child.objects.get(name="Birch release")
    assert (
        client.post(
            reverse("recurring_create", args=[household.pk]),
            {
                "title": "Monday snapshot",
                "child": child.pk,
                "schedule": initial_schedule,
                "weekdays": [0, 2],
            },
        ).status_code
        == 302
    )
    definition = Definition.objects.get(title="Monday snapshot")
    original = Occurrence.objects.get(definition=definition)
    assert original.due_date == date(2026, 10, 26)

    # No browser is needed for scheduler reconciliation. To-do Monday survives
    # later scheduled dates, then awaiting-approval Monday also blocks a backlog.
    instant = instant.replace(day=27)
    call_command("reconcile_recurrence", "--once", verbosity=0)
    assert Occurrence.objects.filter(definition=definition).count() == 1
    assert post_submit(client, household, original).status_code == 302
    original.refresh_from_db()
    assert original.state == "awaiting_approval"
    instant = instant.replace(day=approval_day)
    call_command("reconcile_recurrence", "--once", verbosity=0)
    assert Occurrence.objects.filter(definition=definition).count() == 1
    assert not Approval.objects.filter(occurrence=original).exists()
    authorize()
    edit = reverse("recurring_edit", args=[household.pk, definition.pk])
    assert (
        client.post(
            edit,
            {
                "title": "Future snapshot",
                "child": other.pk,
                "schedule": "weekdays",
                "weekdays": [0, 2, 4],
                "version": definition.version,
            },
        ).status_code
        == 302
    )
    original.refresh_from_db()
    assert (original.title, original.child_id, original.due_date) == (
        "Monday snapshot",
        child.pk,
        date(2026, 10, 26),
    )
    assert post_review(client, household, original).status_code == 302
    original.refresh_from_db()
    assert original.state == "completed"
    assert Approval.objects.filter(occurrence=original).count() == 1
    pending = Occurrence.objects.filter(definition=definition).exclude(
        state="completed"
    )
    assert pending.count() == int(expected_day is not None)
    if expected_day:
        future = pending.get()
        assert (future.title, future.child_id, future.due_date) == (
            "Future snapshot",
            other.pk,
            date(2026, 10, expected_day),
        )
    else:
        # Tuesday is unscheduled; Wednesday creates one next eligible item.
        instant = instant.replace(day=28)
        call_command("reconcile_recurrence", "--once", verbosity=0)
        future = pending.get()
        assert (future.title, future.child_id, future.due_date) == (
            "Future snapshot",
            other.pk,
            date(2026, 10, 28),
        )
        authorize()
    if initial_schedule == "daily":
        assert post_submit(client, household, future, pin="0123").status_code == 302
        future.refresh_from_db()
        mixed = client.get(reverse("household_board", args=[household.pk]))
        assert all(
            text in mixed.content
            for text in (b"To do", b"Awaiting approval", b"Completed")
        )
    # A further schedule/title/assignment edit preserves both current and earned
    # snapshots, and deleting the definition preserves the actual HTTP award.
    definition.refresh_from_db()
    assert (
        client.post(
            edit,
            {
                "title": "Next title",
                "child": child.pk,
                "schedule": "daily",
                "version": definition.version,
            },
        ).status_code
        == 302
    )
    future.refresh_from_db()
    original.refresh_from_db()
    assert future.title == "Future snapshot" and future.child_id == other.pk
    assert original.title == "Monday snapshot" and original.child_id == child.pk
    definition.refresh_from_db()
    assert (
        client.post(
            reverse("recurring_delete", args=[household.pk, definition.pk]),
            {"version": definition.version},
        ).status_code
        == 302
    )
    original.refresh_from_db()
    assert original.definition_id is None and original.state == "completed"
    assert not Occurrence.objects.filter(pk=future.pk).exists()
    instant = instant.replace(day=30)
    call_command("reconcile_recurrence", "--once", verbosity=0)
    assert not Definition.objects.filter(pk=definition.pk).exists()
    assert Approval.objects.filter(occurrence=original).count() == 1
    board = client.get(reverse("household_board", args=[household.pk]))
    assert (
        b"Monday snapshot" in board.content and b"Future snapshot" not in board.content
    )
    by_child = {column.child_id: column.work for column in board.context["columns"]}
    assert (by_child[child.pk].weekly_stars, by_child[child.pk].all_time_stars) == (
        1,
        1,
    )
    assert by_child[other.pk].all_time_stars == 0
