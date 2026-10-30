from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from datetime import timezone as dtz
from threading import Barrier

import pytest
from django.db import OperationalError, close_old_connections
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from accounts.limits import private_key
from accounts.models import AuthenticationLimit
from chores.models import Approval, Occurrence
from chores.recurrence import reconcile_definition, save_recurring
from chores.review import review_work
from chores.services import save_one_off
from households.models import BoardAuthority, Child
from households.pins import save_child_pin
from households.services import Conflict
from tests.integration.test_chores import prepared, values
from tests.integration.test_pins import PASS_B, setup, unlock


def ready():
    a, b, h, c, child = prepared()
    save_child_pin(child, "0007")
    work = save_one_off(
        h, {"title": "Water plants", "child": child, "due_date": date(2026, 10, 27)}
    )
    return a, b, h, c, child, work


def post_submit(c, h, w, **extra):
    return c.post(
        reverse("chore_submit", args=[h.pk, w.pk]),
        {
            "pin": "0007",
            "version": w.version,
            "browser_timezone": "America/Los_Angeles",
            **extra,
        },
    )


def post_review(c, h, w, **extra):
    return c.post(
        reverse("chore_review", args=[h.pk, w.pk]),
        {"version": w.version, "action": "approve", **extra},
    )


@pytest.mark.django_db
def test_submit_return_resubmit_either_parent_approve_and_retry():
    a, b, h, c, child, w = ready()
    original_activity = BoardAuthority.objects.get().last_activity
    assert post_submit(c, h, w).status_code == 302
    assert BoardAuthority.objects.get().last_activity == original_activity
    w.refresh_from_db()
    assert (
        w.state == "awaiting_approval"
        and w.submitted_at
        and not Approval.objects.exists()
    )
    assert post_submit(c, h, w).status_code == 409
    for note in ("", " \n "):
        assert post_review(c, h, w, action="return", note=note).status_code == 400
    assert (
        post_review(
            c, h, w, action="return", note="Please water the small pot too."
        ).status_code
        == 302
    )
    w.refresh_from_db()
    assert (
        w.state == "to_do"
        and w.submitted_late is None
        and not Approval.objects.exists()
    )
    assert (
        b"Please water the small pot too."
        in c.get(reverse("household_board", args=[h.pk])).content
    )
    assert post_submit(c, h, w).status_code == 302
    w.refresh_from_db()
    setup(c, h, b, password=PASS_B, pin="1234")
    unlock(c, h, b, pin="1234")
    version = w.version
    assert post_review(c, h, w).status_code == 302
    w.refresh_from_db()
    award = Approval.objects.get(occurrence=w)
    assert (
        w.state == "completed"
        and award.parent == b
        and award.approved_at == w.completed_at
    )
    # The first committed response may be lost; replaying its exact body is honest conflict.
    assert post_review(c, h, w, version=version).status_code == 409
    assert Approval.objects.count() == 1
    c.logout()
    c.force_login(a)
    assert Approval.objects.get().occurrence.state == "completed"


@pytest.mark.django_db
@pytest.mark.parametrize("state", ["to_do", "awaiting_approval", "completed"])
def test_wrong_pin_limit_commits_even_for_denied_transition_shared_exact_expiry(
    monkeypatch, state
):
    a, _, h, c, child, w = ready()
    w.state = state
    w.save()
    now = timezone.now()
    monkeypatch.setattr("django.utils.timezone.now", lambda: now)
    other = Client()
    other.force_login(a)
    for index in range(5):
        assert (
            post_submit(c if index % 2 else other, h, w, pin="1234").status_code == 400
        )
    limit = AuthenticationLimit.objects.get(key=private_key("child-pin", str(child.pk)))
    assert limit.failures == 5 and limit.blocked_until == now + timedelta(minutes=5)
    deadline = limit.blocked_until
    now += timedelta(seconds=299)
    assert post_submit(other, h, w).status_code == 400
    limit.refresh_from_db()
    assert limit.blocked_until == deadline
    now += timedelta(seconds=1)
    assert post_submit(other, h, w).status_code == (302 if state == "to_do" else 409)
    limit.refresh_from_db()
    assert limit.failures == 0 and limit.blocked_until is None
    assert not Approval.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "zone,instant,late",
    [
        ("America/Los_Angeles", "2026-10-28T01:00:00+00:00", False),
        ("Asia/Tokyo", "2026-10-28T01:00:00+00:00", True),
        ("Europe/Warsaw", "2026-10-27T22:59:59+00:00", False),
        ("Europe/Warsaw", "2026-10-27T23:00:00+00:00", True),
        ("America/Los_Angeles", "2026-11-01T08:30:00+00:00", False),
        ("America/Los_Angeles", "2026-11-01T09:30:00+00:00", False),
    ],
)
def test_server_receipt_zone_midnight_dst_and_return_reclassification(
    monkeypatch, zone, instant, late
):
    _, _, h, c, _, w = ready()
    if "11-01" in instant:
        w.due_date = date(2026, 11, 1)
        w.save()
    now = datetime.fromisoformat(instant)
    monkeypatch.setattr("django.utils.timezone.now", lambda: now)
    assert (
        post_submit(
            c, h, w, browser_timezone=zone, client_clock="1900-01-01"
        ).status_code
        == 302
    )
    w.refresh_from_db()
    assert (
        w.submitted_late is late
        and w.submitted_at == now
        and w.submitted_timezone == zone
    )
    now += timedelta(days=2)
    board = c.get(reverse("household_board", args=[h.pk])).content
    assert f'data-submitted-late="{str(late).lower()}"'.encode() in board
    assert w.submitted_late is late
    # Re-unlock after simulated elapsed days; return restores ordinary local-date rule.
    unlock(c, h, h.memberships.first().user)
    assert post_review(c, h, w, action="return", note="Try again").status_code == 302
    w.refresh_from_db()
    assert w.submitted_late is None
    assert post_submit(c, h, w, browser_timezone=zone).status_code == 302
    w.refresh_from_db()
    assert w.submitted_late is True


@pytest.mark.django_db
@pytest.mark.parametrize("zone", ["", "Mars/Imaginary", "../UTC"])
def test_invalid_timezone_no_mutation(zone):
    _, _, h, c, _, w = ready()
    assert post_submit(c, h, w, browser_timezone=zone).status_code == 400
    w.refresh_from_db()
    assert w.state == "to_do" and w.submitted_at is None


@pytest.mark.django_db
def test_child_other_pin_role_isolation_csrf_and_no_echo(monkeypatch, caplog):
    a, _, h, c, child, w = ready()
    other = Child.objects.create(household=h, name="Birch", pin_hash="")
    save_child_pin(other, "0123")
    response = post_submit(c, h, w, pin="0123")
    assert response.status_code == 400 and b'value="0123"' not in response.content
    locked = Client()
    locked.force_login(a)
    assert post_review(locked, h, w).status_code == 403
    assert post_submit(locked, h, w).status_code == 302
    w.refresh_from_db()
    assert post_review(locked, h, w, pin="0007").status_code == 403
    csrf = Client(enforce_csrf_checks=True)
    csrf.force_login(a)
    assert post_submit(csrf, h, w).status_code == 403
    assert post_review(csrf, h, w).status_code == 403
    from allauth.account.models import EmailAddress
    from django.contrib.auth import get_user_model

    from households.services import create_household

    outsider = get_user_model().objects.create_user(
        username="foreign", email="foreign@example.test"
    )
    EmailAddress.objects.create(user=outsider, email=outsider.email, verified=True)
    foreign = create_household(outsider, "UTC")
    for route in ("chore_submit", "chore_review"):
        assert (
            c.post(reverse(route, args=[foreign.pk, w.pk]), {"pin": "0007"}).status_code
            == 403
        )
        outside = Client()
        outside.force_login(outsider)
        assert outside.get(reverse(route, args=[h.pk, w.pk])).status_code == 403
        assert c.post(reverse(route, args=[h.pk, 999999])).status_code == 409
    monkeypatch.setattr(
        "chores.review.Approval.objects.create",
        lambda **kw: (_ for _ in ()).throw(
            OperationalError("private synthetic DB error")
        ),
    )
    response = post_review(c, h, w)
    assert (
        response.status_code == 503
        and b"private synthetic DB error" not in response.content
    )
    w.refresh_from_db()
    assert w.state == "awaiting_approval" and not Approval.objects.exists()
    assert "private synthetic DB error" not in caplog.text


@pytest.mark.django_db
@pytest.mark.parametrize(
    "schedule,day,expected",
    [
        ("daily", 28, 28),
        ("weekdays", 28, 28),
        ("weekdays", 27, None),
        ("daily", 26, None),
    ],
)
def test_actual_approval_recurrence_atomic_no_backlog_retained_awards(
    schedule, day, expected
):
    a, _, h, c, child, _ = ready()
    now = datetime(2026, 10, 26, 10, tzinfo=dtz.utc)
    definition = save_recurring(
        h,
        {
            "title": "Recurring",
            "child": child,
            "schedule": schedule,
            "weekdays": [0, 2],
        },
        now=now,
    )
    work = Occurrence.objects.get(definition=definition)
    assert post_submit(c, h, work).status_code == 302
    work.refresh_from_db()
    review_work(h, work.pk, work.version, a, "approve", now=now.replace(day=day))
    pending = Occurrence.objects.filter(definition=definition).exclude(
        state="completed"
    )
    assert pending.count() == (expected is not None)
    if expected:
        assert pending.get().due_date.day == expected
    definition.refresh_from_db()
    save_recurring(h, {"version": definition.version}, definition.pk, delete=True)
    work.refresh_from_db()
    assert (
        work.definition_id is None
        and work.state == "completed"
        and Approval.objects.filter(occurrence=work).count() == 1
    )


@pytest.mark.django_db
def test_p03_after_real_return_edit_delete_and_completed_retention():
    _, _, h, c, child, w = ready()
    post_submit(c, h, w)
    w.refresh_from_db()
    assert (
        c.post(
            reverse("chore_delete", args=[h.pk, w.pk]), {"version": w.version}
        ).status_code
        == 409
    )
    post_review(c, h, w, action="return", note="More water")
    w.refresh_from_db()
    assert (
        c.post(
            reverse("chore_edit", args=[h.pk, w.pk]), values(child, version=w.version)
        ).status_code
        == 302
    )
    w.refresh_from_db()
    post_submit(c, h, w)
    w.refresh_from_db()
    post_review(c, h, w)
    w.refresh_from_db()
    assert (
        c.post(
            reverse("chore_delete", args=[h.pk, w.pk]), {"version": w.version}
        ).status_code
        == 409
    )
    assert Approval.objects.filter(occurrence=w).exists()
    second = save_one_off(
        h, {"title": "Returned then deleted", "child": child, "due_date": date.today()}
    )
    post_submit(c, h, second)
    second.refresh_from_db()
    post_review(c, h, second, action="return", note="No longer needed")
    second.refresh_from_db()
    assert (
        c.post(
            reverse("chore_delete", args=[h.pk, second.pk]), {"version": second.version}
        ).status_code
        == 302
    )
    assert Approval.objects.count() == 1


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    "opponent", ["approve", "return", "delete", "scheduler", "edit"]
)
def test_competing_independent_transactions(opponent):
    a, _, h, c, child, _ = ready()
    now = datetime(2026, 10, 26, 10, tzinfo=dtz.utc)
    definition = save_recurring(
        h,
        {"title": "Race", "child": child, "schedule": "daily", "weekdays": []},
        now=now,
    )
    w = Occurrence.objects.get(definition=definition)
    post_submit(c, h, w)
    w.refresh_from_db()
    gate = Barrier(2)

    def run(action):
        close_old_connections()
        try:
            gate.wait(timeout=10)
            try:
                if action == "delete":
                    save_recurring(h, {"version": 1}, definition.pk, delete=True)
                elif action == "edit":
                    save_recurring(
                        h,
                        {
                            "version": 1,
                            "title": "Future edit",
                            "child": child,
                            "schedule": "daily",
                            "weekdays": [],
                        },
                        definition.pk,
                    )
                elif action == "scheduler":
                    reconcile_definition(definition.pk, now=now + timedelta(days=2))
                else:
                    review_work(
                        h,
                        w.pk,
                        w.version,
                        a,
                        action,
                        "More water",
                        now=now + timedelta(days=2),
                    )
                return "accepted"
            except (
                Conflict,
                __import__(
                    "django.core.exceptions", fromlist=["PermissionDenied"]
                ).PermissionDenied,
            ):
                return "conflict"
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, ["approve", opponent]))
    if opponent in ("approve", "return"):
        assert sorted(results) == ["accepted", "conflict"]
    if opponent in ("edit", "scheduler"):
        assert results == ["accepted", "accepted"]
        assert Approval.objects.count() == 1
        completed = Occurrence.objects.get(pk=w.pk)
        assert completed.title == "Race" and completed.state == "completed"
        assert Occurrence.objects.filter(definition=definition).exclude(
            state="completed"
        ).get().due_date == date(2026, 10, 28)
    assert Approval.objects.count() <= 1
    assert (
        Occurrence.objects.filter(definition=definition)
        .exclude(state="completed")
        .count()
        <= 1
    )
    if Approval.objects.exists():
        assert Approval.objects.get().occurrence.state == "completed"


@pytest.mark.django_db(transaction=True)
def test_fresh_process_restart_retains_actual_awards_and_deleted_recurrence():
    import json
    import os
    import subprocess
    import sys

    from django.db import connection

    a, _, h, c, child, w = ready()
    assert post_submit(c, h, w).status_code == 302
    w.refresh_from_db()
    assert post_review(c, h, w).status_code == 302
    definition = save_recurring(
        h,
        {
            "title": "Retained earned history",
            "child": child,
            "schedule": "daily",
            "weekdays": [],
        },
    )
    recurring = Occurrence.objects.get(definition=definition)
    assert post_submit(c, h, recurring).status_code == 302
    recurring.refresh_from_db()
    review_work(h, recurring.pk, recurring.version, a, "approve")
    definition.refresh_from_db()
    save_recurring(h, {"version": definition.version}, definition.pk, delete=True)
    env = dict(
        os.environ,
        DJANGO_SETTINGS_MODULE="config.settings.local",
        DB_NAME=connection.settings_dict["NAME"],
    )
    probe = f"import django; django.setup(); import json; from chores.models import Approval, Occurrence; print(json.dumps([Approval.objects.count(), Occurrence.objects.get(pk={recurring.pk}).definition_id, Occurrence.objects.get(pk={w.pk}).state]))"
    for _ in range(2):
        result = subprocess.run(
            [sys.executable, "-c", probe],
            env=env,
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
        )
        assert json.loads(result.stdout.strip()) == [2, None, "completed"]


@pytest.mark.django_db
def test_approval_failure_rolls_back_recurrence_star_state_revision_and_retry(
    monkeypatch,
):
    a, _, h, c, child, _ = ready()
    now = datetime(2026, 10, 26, 10, tzinfo=dtz.utc)
    definition = save_recurring(
        h,
        {"title": "Atomic", "child": child, "schedule": "daily", "weekdays": []},
        now=now,
    )
    work = Occurrence.objects.get(definition=definition)
    post_submit(c, h, work)
    work.refresh_from_db()
    h.refresh_from_db()
    revision = h.revision
    original = Approval.objects.create

    def fail(**kwargs):
        raise OperationalError("Synthetic unavailable database")

    monkeypatch.setattr(Approval.objects, "create", fail)
    with pytest.raises(OperationalError):
        review_work(h, work.pk, work.version, a, "approve", now=now + timedelta(days=2))
    work.refresh_from_db()
    h.refresh_from_db()
    definition.refresh_from_db()
    assert work.state == "awaiting_approval" and work.completed_at is None
    assert Occurrence.objects.filter(definition=definition).count() == 1
    assert not Approval.objects.exists() and h.revision == revision
    assert definition.eligible_from == now.date()
    monkeypatch.setattr(Approval.objects, "create", original)
    review_work(h, work.pk, work.version, a, "approve", now=now + timedelta(days=2))
    assert Approval.objects.count() == 1
    assert Occurrence.objects.filter(definition=definition).count() == 2


@pytest.mark.django_db
def test_lost_committed_approval_response_retry_refreshes_without_extra_star(
    monkeypatch,
):
    _, _, h, c, _, w = ready()
    post_submit(c, h, w)
    w.refresh_from_db()
    deliver = c.handler.get_response

    def lose_response(request):
        response = deliver(request)
        assert response.status_code == 302
        raise ConnectionAbortedError("Synthetic lost response after commit")

    with monkeypatch.context() as patch:
        patch.setattr(c.handler, "get_response", lose_response)
        with pytest.raises(ConnectionAbortedError):
            post_review(c, h, w)
    response = post_review(c, h, w)
    assert response.status_code == 409 and b"current board is shown" in response.content
    assert Approval.objects.filter(occurrence=w).count() == 1
    w.refresh_from_db()
    assert w.state == "completed"


@pytest.mark.django_db
def test_deleted_or_foreign_work_post_shows_scoped_current_board():
    _, _, h, c, _, w = ready()
    identity = w.pk
    w.delete()
    for route in ("chore_submit", "chore_review"):
        response = c.post(
            reverse(route, args=[h.pk, identity]), {"pin": "0007", "version": 1}
        )
        assert response.status_code == 409
        assert (
            b"Check the current board" in response.content
            and b'value="0007"' not in response.content
        )
        assert b'aria-label="Household chore board"' in response.content


@pytest.mark.django_db
def test_assignment_changed_after_pin_verification_cannot_submit_new_child_work(
    monkeypatch,
):
    from chores.review import submit_work

    _, _, h, c, _, w = ready()
    other = Child.objects.create(household=h, name="Birch", pin_hash="")
    save_child_pin(other, "0123")

    def changed(*args):
        save_one_off(
            h,
            {
                "title": w.title,
                "child": other,
                "due_date": w.due_date,
                "version": w.version,
            },
            w.pk,
        )
        return submit_work(*args)

    monkeypatch.setattr("chores.review.submit_work", changed)
    response = post_submit(c, h, w)
    assert response.status_code == 409 and b"Birch" in response.content
    w.refresh_from_db()
    assert w.child == other and w.state == "to_do" and not Approval.objects.exists()


@pytest.mark.django_db
def test_expired_parent_cannot_review_and_child_activity_never_extends():
    _, _, h, c, _, w = ready()
    BoardAuthority.objects.update(last_activity=timezone.now() - timedelta(seconds=60))
    before = BoardAuthority.objects.get().last_activity
    assert post_submit(c, h, w).status_code == 302
    w.refresh_from_db()
    assert post_review(c, h, w).status_code == 403
    assert BoardAuthority.objects.get().last_activity == before
    assert not Approval.objects.exists()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("mode", ["submit", "approve"])
def test_simultaneous_http_requests_across_independent_board_sessions(mode):
    a, _, h, c, _, w = ready()
    second = Client()
    second.force_login(a)
    unlock(second, h, a)
    if mode == "approve":
        assert post_submit(c, h, w).status_code == 302
        w.refresh_from_db()
    gate = Barrier(2)

    def run(client):
        close_old_connections()
        try:
            gate.wait(timeout=10)
            return (
                post_submit(client, h, w)
                if mode == "submit"
                else post_review(client, h, w)
            ).status_code
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as pool:
        statuses = list(pool.map(run, [c, second]))
    assert sorted(statuses) == [302, 409]
    w.refresh_from_db()
    assert w.state == ("completed" if mode == "approve" else "awaiting_approval")
    assert Approval.objects.count() == (1 if mode == "approve" else 0)
