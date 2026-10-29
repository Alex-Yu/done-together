from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from io import StringIO
from threading import Barrier
from unittest.mock import patch

import pytest
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import (
    IntegrityError,
    OperationalError,
    close_old_connections,
    transaction,
)
from django.urls import reverse

from chores.models import Definition, Occurrence
from chores.recurrence import (
    complete_occurrence,
    reconcile_all,
    reconcile_definition,
    save_recurring,
)
from households.models import Child
from households.services import Conflict
from tests.integration.test_chores import prepared


def instant(day, hour=12):
    return datetime(2026, 10, day, hour, tzinfo=timezone.utc)


def data(child, **extra):
    return dict(title="Feed fish", child=child, schedule="daily", weekdays=[], **extra)


def make(h, child, day=19, schedule="daily", weekdays=None):
    return save_recurring(
        h,
        data(child) | dict(schedule=schedule, weekdays=weekdays or []),
        now=instant(day),
    )


def finish(h, work, day):
    work.state = "awaiting_approval"
    work.save()
    return complete_occurrence(h, work.pk, work.version, instant(day))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "schedule,weekdays,initial,next_day",
    [("daily", [], 19, 20), ("weekdays", [2, 4], None, 21)],
)
def test_initial_calendar_and_recovery(schedule, weekdays, initial, next_day):
    _, _, h, _, child = prepared()
    definition = make(h, child, schedule=schedule, weekdays=weekdays)
    assert list(Occurrence.objects.values_list("due_date__day", flat=True)) == (
        [initial] if initial else []
    )
    if initial:
        finish(h, Occurrence.objects.get(), 19)
    assert reconcile_all(instant(19)) == 0
    assert reconcile_all(instant(next_day)) == 1
    work = Occurrence.objects.exclude(state="completed").get()
    assert work.due_date.day == next_day
    assert reconcile_all(instant(25)) == 0  # unfinished spans scheduled days
    work.state = "awaiting_approval"
    work.save()
    assert reconcile_all(instant(26)) == 0
    complete_occurrence(h, work.pk, work.version, instant(26))
    if schedule == "daily":
        assert Occurrence.objects.exclude(state="completed").get().due_date.day == 26
    else:
        assert not Occurrence.objects.exclude(state="completed").exists()
    assert definition.pk


@pytest.mark.django_db
def test_latest_recovery_no_backlog_no_precreation():
    _, _, h, _, child = prepared()
    make(h, child, day=20, schedule="weekdays", weekdays=[2, 4])
    assert reconcile_all(instant(19)) == 0
    assert reconcile_all(instant(26)) == 1
    assert Occurrence.objects.get().due_date.day == 23
    assert reconcile_all(instant(26)) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("day, expected", [(21, 21), (20, None)])
def test_late_completion_fixed_schedule_and_no_today_duplicate(day, expected):
    _, _, h, _, child = prepared()
    make(h, child, schedule="weekdays", weekdays=[0, 2])
    work = Occurrence.objects.get()
    completed = finish(h, work, day)
    assert completed.state == "completed" and completed.due_date.day == 19
    assert reconcile_all(instant(day)) == 0
    active = Occurrence.objects.exclude(state="completed")
    assert list(active.values_list("due_date__day", flat=True)) == (
        [expected] if expected else []
    )
    if expected:
        finish(h, active.get(), day)
        assert reconcile_all(instant(day)) == 0
    else:
        assert reconcile_all(instant(21)) == 1
    with pytest.raises(Conflict):
        complete_occurrence(h, work.pk, 1, instant(day))


@pytest.mark.django_db
@pytest.mark.parametrize("state", ["to_do", "awaiting_approval"])
def test_future_snapshots_delete_retains_completed(state):
    _, _, h, _, child = prepared()
    definition = make(h, child)
    finish(h, Occurrence.objects.get(), 19)
    reconcile_all(instant(20))
    current = Occurrence.objects.exclude(state="completed").get()
    current.state = state
    current.save()
    other = Child.objects.create(household=h, name="Birch", pin_hash="synthetic")
    save_recurring(
        h,
        data(other)
        | dict(title="New title", schedule="weekdays", weekdays=[2], version=1),
        definition.pk,
        now=instant(20),
    )
    current.refresh_from_db()
    assert (
        current.title == "Feed fish"
        and current.child == child
        and current.due_date.day == 20
    )
    current.state = "awaiting_approval"
    current.save()
    complete_occurrence(h, current.pk, 1, instant(21))
    future = Occurrence.objects.exclude(state="completed").get()
    assert (
        future.title == "New title"
        and future.child == other
        and future.due_date.day == 21
    )
    future.state = state
    future.save()
    save_recurring(h, {"version": 2}, definition.pk, delete=True)
    assert not Definition.objects.exists()
    assert Occurrence.objects.count() == 2
    assert not Occurrence.objects.exclude(state="completed").exists()
    assert all(
        w.definition_id is None and w.child == child for w in Occurrence.objects.all()
    )
    assert reconcile_all(instant(28)) == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "now, expected",
    [
        (datetime(2026, 3, 28, 23, 30, tzinfo=timezone.utc), "2026-03-29"),
        (datetime(2026, 3, 29, 22, 30, tzinfo=timezone.utc), "2026-03-30"),
        (datetime(2026, 10, 24, 22, 30, tzinfo=timezone.utc), "2026-10-25"),
        (datetime(2026, 10, 25, 23, 30, tzinfo=timezone.utc), "2026-10-26"),
    ],
)
def test_household_midnight_dst(now, expected):
    _, _, h, _, child = prepared()
    assert h.timezone == "Europe/Warsaw"
    save_recurring(h, data(child), now=now)
    assert str(Occurrence.objects.get().due_date) == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "bad",
    [
        {"title": ""},
        {"child": ""},
        {"child": 999999},
        {"schedule": "once"},
        {"schedule": "weekdays", "weekdays": []},
        {"weekdays": [7]},
        {"weekdays": ["bad"]},
    ],
)
def test_http_validation_atomic(bad):
    _, _, h, client, child = prepared()
    payload = data(child) | {"child": child.pk} | bad
    assert (
        client.post(reverse("recurring_create", args=[h.pk]), payload).status_code
        == 400
    )
    assert not Definition.objects.exists() and not Occurrence.objects.exists()


@pytest.mark.django_db
def test_http_permissions_stale_recovery_persistence(monkeypatch):
    from django.test import Client

    from tests.integration.test_pins import unlock

    parent, _, h, client, child = prepared()
    new = reverse("recurring_create", args=[h.pk])
    payload = data(child) | {"child": child.pk}
    assert client.post(new, payload).status_code == 302
    definition = Definition.objects.get()
    edit = reverse("recurring_edit", args=[h.pk, definition.pk])
    delete = reverse("recurring_delete", args=[h.pk, definition.pk])
    assert (
        client.post(edit, payload | {"title": "Edited", "version": 1}).status_code
        == 302
    )
    assert client.post(edit, payload | {"version": 1}).status_code == 409
    assert client.post(delete, {"version": 1}).status_code == 409
    locked = Client()
    locked.force_login(parent)
    assert locked.post(new, payload).status_code == 403
    csrf = Client(enforce_csrf_checks=True)
    csrf.force_login(parent)
    assert csrf.post(delete, {"version": 2}).status_code == 403
    from allauth.account.models import EmailAddress
    from django.contrib.auth import get_user_model

    from households.services import create_household

    outsider = get_user_model().objects.create_user(
        username="outside", email="outside@example.test"
    )
    EmailAddress.objects.create(user=outsider, email=outsider.email, verified=True)
    foreign = create_household(outsider, "UTC")
    foreign_child = Child.objects.create(
        household=foreign, name="Other", pin_hash="synthetic"
    )
    outside = Client()
    outside.force_login(outsider)
    assert outside.get(edit).status_code == 403
    assert client.post(new, payload | {"child": foreign_child.pk}).status_code == 400
    assert (
        outside.post(
            reverse("recurring_edit", args=[foreign.pk, definition.pk]),
            payload | {"version": 2},
        ).status_code
        == 403
    )
    client.logout()
    client.force_login(parent)
    assert b"Feed fish" in client.get(reverse("household_board", args=[h.pk])).content
    unlock(client, h, parent)
    monkeypatch.setattr(
        "chores.recurrence.save_recurring",
        lambda *a: (_ for _ in ()).throw(OperationalError()),
    )
    assert client.post(edit, payload | {"version": 2}).status_code == 503
    assert Definition.objects.get(pk=definition.pk).title == "Edited"


@pytest.mark.django_db
def test_database_invariants():
    _, _, h, _, child = prepared()
    definition = make(h, child)
    work = Occurrence.objects.get()
    for day in [19, 20]:
        with pytest.raises(IntegrityError), transaction.atomic():
            Occurrence.objects.create(
                definition=definition,
                household=h,
                child=child,
                title="Duplicate",
                due_date=instant(day).date(),
            )
    work.state = "completed"
    work.save()
    with pytest.raises(IntegrityError), transaction.atomic():
        Occurrence.objects.create(
            definition=definition,
            household=h,
            child=child,
            title="Duplicate date",
            due_date=work.due_date,
        )


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    "pair",
    [
        ("scheduler", "scheduler"),
        ("scheduler", "completion"),
        ("scheduler", "delete"),
        ("scheduler", "edit"),
        ("edit", "completion"),
        ("delete", "completion"),
    ],
)
def test_independent_transaction_races(pair):
    _, _, h, _, child = prepared()
    definition = make(h, child)
    work = Occurrence.objects.get()
    work.state = "awaiting_approval"
    work.save()
    if pair in [
        ("scheduler", "scheduler"),
        ("scheduler", "edit"),
        ("scheduler", "delete"),
    ]:
        finish(h, work, 19)
    gate = Barrier(2)

    def run(action):
        close_old_connections()
        try:
            gate.wait(timeout=10)
            if action == "scheduler":
                reconcile_definition(definition.pk, instant(21))
            elif action == "completion":
                complete_occurrence(h, work.pk, 1, instant(21))
            else:
                save_recurring(
                    h,
                    data(child) | {"title": "Edited", "version": 1},
                    definition.pk,
                    action == "delete",
                    now=instant(21),
                )
            return "accepted"
        except (Conflict, PermissionDenied):
            return "conflict"
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, pair))
    assert "accepted" in results
    assert Occurrence.objects.exclude(state="completed").count() <= 1
    assert Occurrence.objects.filter(state="completed").count() <= 1
    if not Definition.objects.exists():
        assert not Occurrence.objects.exclude(state="completed").exists()
    else:
        for item in Occurrence.objects.all():
            assert (
                Occurrence.objects.filter(
                    definition=item.definition, due_date=item.due_date
                ).count()
                == 1
            )


@pytest.mark.django_db(transaction=True)
def test_command_safe_retry_and_interrupt():
    out, err = StringIO(), StringIO()
    call_command("reconcile_recurrence", once=True, stdout=out)
    assert "Reconciled: 0" in out.getvalue()
    with patch(
        "chores.management.commands.reconcile_recurrence.reconcile_all",
        side_effect=OperationalError(),
    ):
        with pytest.raises(CommandError, match="retry safely"):
            call_command("reconcile_recurrence", once=True)
    with (
        patch(
            "chores.management.commands.reconcile_recurrence.reconcile_all",
            side_effect=[OperationalError(), 1],
        ),
        patch(
            "chores.management.commands.reconcile_recurrence.time.sleep",
            side_effect=[None, KeyboardInterrupt],
        ) as sleep,
    ):
        call_command(
            "reconcile_recurrence", loop=True, interval=60, stdout=out, stderr=err
        )
    assert sleep.call_args.args == (60,)
    assert (
        "retrying" in err.getvalue()
        and "Reconciled: 1" in out.getvalue()
        and "stopped cleanly" in out.getvalue()
    )


@pytest.mark.django_db(transaction=True)
def test_real_no_browser_once_loop_sixty_restart(tmp_path):
    """Actual subprocess/PG persistence; no web server or browser is running."""
    import os
    import signal
    import subprocess
    import sys
    import time

    from django.db import connection
    from django.utils import timezone as django_timezone

    from chores.recurrence import local_date

    _, _, h, _, child = prepared()
    definition = save_recurring(h, data(child), now=django_timezone.now())
    Occurrence.objects.all().delete()  # synthetic downtime gap, not a product action
    env = dict(
        os.environ,
        DJANGO_SETTINGS_MODULE="config.settings.local",
        DB_NAME=connection.settings_dict["NAME"],
    )
    command = [sys.executable, "manage.py", "reconcile_recurrence"]
    result = subprocess.run(
        command + ["--once"], env=env, capture_output=True, timeout=15
    )
    assert result.returncode == 0 and b"Reconciled: 1" in result.stdout
    identity = Occurrence.objects.get().pk
    result = subprocess.run(
        command + ["--once"], env=env, capture_output=True, timeout=15
    )
    assert result.returncode == 0 and b"Reconciled: 0" in result.stdout
    assert Occurrence.objects.get().pk == identity
    log = tmp_path / "scheduler.txt"
    with log.open("w") as output:
        process = subprocess.Popen(
            command + ["--loop", "--interval", "60"],
            env=env,
            stdout=output,
            stderr=output,
        )
        try:
            deadline = time.monotonic() + 15
            while "Reconciled: 0" not in log.read_text():
                assert process.poll() is None and time.monotonic() < deadline
                time.sleep(0.1)
            Occurrence.objects.all().delete()  # no unfinished work when next tick runs
            started = time.monotonic()
            deadline = started + 70
            while not Occurrence.objects.exists():
                assert process.poll() is None and time.monotonic() < deadline
                time.sleep(0.2)
            assert time.monotonic() - started >= 58
            assert Occurrence.objects.get().due_date == local_date(h)
        finally:
            process.send_signal(signal.SIGINT)
            process.wait(timeout=10)
    assert process.returncode == 0 and "Scheduler stopped cleanly." in log.read_text()
    # Fresh scheduler process observes persisted definition/work, without browser startup.
    result = subprocess.run(
        command + ["--once"], env=env, capture_output=True, timeout=15
    )
    assert result.returncode == 0 and b"Reconciled: 0" in result.stdout
    assert Definition.objects.get(pk=definition.pk).title == "Feed fish"


@pytest.mark.django_db(transaction=True)
def test_real_scheduler_connection_failure_then_restart():
    import os
    import subprocess
    import sys

    from django.db import connection

    env = dict(
        os.environ,
        DJANGO_SETTINGS_MODULE="config.settings.local",
        DB_NAME=connection.settings_dict["NAME"],
    )
    command = [sys.executable, "manage.py", "reconcile_recurrence", "--once"]
    failed = subprocess.run(
        command, env=env | {"DB_PORT": "1"}, capture_output=True, timeout=15
    )
    assert failed.returncode != 0
    assert b"Scheduling unavailable; retry safely." in failed.stderr
    assert b"Traceback" not in failed.stderr and b"PASSWORD" not in failed.stderr
    recovered = subprocess.run(command, env=env, capture_output=True, timeout=15)
    assert recovered.returncode == 0 and b"Reconciled: 0" in recovered.stdout
