from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from threading import Barrier

import pytest
from django.db import close_old_connections
from django.urls import reverse

from board.read_model import columns_for_household, household_week
from chores.models import Approval, Occurrence
from chores.review import review_work
from chores.services import save_one_off
from households.services import Conflict
from tests.integration.test_review import post_review, post_submit, ready


def approve(h, c, a, child, title, instant, due=date(2026, 10, 25)):
    work = save_one_off(h, {"title": title, "child": child, "due_date": due})
    assert post_submit(c, h, work).status_code == 302
    work.refresh_from_db()
    review_work(h, work.pk, work.version, a, "approve", now=instant)
    return work


@pytest.mark.django_db
@pytest.mark.parametrize("viewer_zone", ["America/Los_Angeles", "Asia/Tokyo"])
def test_approval_week_rollover_old_active_and_totals(monkeypatch, viewer_zone):
    from django.utils import timezone as django_timezone

    a, _, h, c, child, active = ready()
    # Viewer timezone must not change household calendar membership.
    now, _ = household_week(h, datetime(2026, 10, 26, 12, tzinfo=timezone.utc))
    before = approve(
        h, c, a, child, "Prior completion", now - timedelta(microseconds=1)
    )
    sunday = approve(h, c, a, child, "Sunday approved Monday", now)
    url = reverse("household_board", args=[h.pk])
    monkeypatch.setattr("django.utils.timezone.now", lambda: now)
    with django_timezone.override(viewer_zone):
        result = c.get(url)
        work = result.context["columns"][0].work
        assert (work.weekly_stars, work.all_time_stars) == (1, 2)
        assert [x.identity for x in work.completed_this_week] == [str(sunday.pk)]
        assert str(active.pk) in [x.identity for x in work.active]
        body = result.content.decode()
        assert "Sunday approved Monday" in body and "Prior completion" not in body
        assert "This week: 1 star" in body and "All time: 2 stars" in body
        assert "<details" not in body
    now += timedelta(days=7)
    result = c.get(url)
    work = result.context["columns"][0].work
    assert (work.weekly_stars, work.all_time_stars) == (0, 2)
    assert not work.completed_this_week and len(work.active) == 1
    assert Occurrence.objects.filter(pk__in=[before.pk, sunday.pk]).count() == 2
    c.logout()
    c.force_login(a)
    assert c.get(url).context["columns"][0].work.all_time_stars == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    "monday,hours", [(date(2026, 3, 23), 167), (date(2026, 10, 19), 169)]
)
def test_warsaw_dst_calendar_week_exact_boundaries(monkeypatch, monday, hours):
    from households.models import Household

    a, _, h, c, child, _ = ready()
    # Separate immutable timezone setup fixture, no product timezone-changing control.
    Household.objects.filter(pk=h.pk).update(timezone="Europe/Warsaw")
    h.refresh_from_db()
    noon = datetime.combine(monday, datetime.min.time(), timezone.utc) + timedelta(
        hours=12
    )
    start, end = household_week(h, noon)
    assert (
        end.astimezone(timezone.utc) - start.astimezone(timezone.utc)
    ).total_seconds() == hours * 3600
    for title, instant in [
        ("Before", start - timedelta(microseconds=1)),
        ("Start", start),
        ("Last", end - timedelta(microseconds=1)),
        ("Next", end),
    ]:
        approve(h, c, a, child, title, instant)
    monkeypatch.setattr("django.utils.timezone.now", lambda: noon)
    work = columns_for_household(h)[0].work
    assert (work.weekly_stars, work.all_time_stars) == (2, 4)
    assert [x.title for x in work.completed_this_week] == ["Start", "Last"]
    monkeypatch.setattr("django.utils.timezone.now", lambda: end)
    work = columns_for_household(h)[0].work
    assert (work.weekly_stars, work.all_time_stars) == (1, 4)
    assert [x.title for x in work.completed_this_week] == ["Next"]


@pytest.mark.django_db
def test_submit_return_zero_and_retry_one_visible_award():
    a, _, h, c, child, work = ready()
    assert post_submit(c, h, work).status_code == 302
    work.refresh_from_db()
    assert columns_for_household(h)[0].work.all_time_stars == 0
    assert post_review(c, h, work, action="return", note="Try again").status_code == 302
    work.refresh_from_db()
    assert columns_for_household(h)[0].work.all_time_stars == 0
    assert post_submit(c, h, work).status_code == 302
    work.refresh_from_db()
    assert post_review(c, h, work).status_code == 302
    assert post_review(c, h, work).status_code == 409
    visible = columns_for_household(h)[0].work
    assert (visible.weekly_stars, visible.all_time_stars) == (1, 1)
    assert len(visible.completed_this_week) == 1


@pytest.mark.django_db(transaction=True)
def test_concurrent_actual_approvals_one_visible_star():
    a, _, h, c, child, work = ready()
    assert post_submit(c, h, work).status_code == 302
    work.refresh_from_db()
    gate = Barrier(2)

    def run(_):
        close_old_connections()
        try:
            gate.wait(timeout=10)
            try:
                review_work(h, work.pk, work.version, a, "approve")
                return "approved"
            except Conflict:
                return "conflict"
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(run, range(2))) == ["approved", "conflict"]
    visible = columns_for_household(h)[0].work
    assert (visible.weekly_stars, visible.all_time_stars) == (1, 1)
    assert len(visible.completed_this_week) == Approval.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_deleted_recurrence_projected_history_survives_fresh_processes():
    import json
    import os
    import subprocess
    import sys

    from django.db import connection

    from chores.recurrence import save_recurring

    a, _, h, c, child, _ = ready()
    definition = save_recurring(
        h,
        {
            "title": "Retained approval",
            "child": child,
            "schedule": "daily",
            "weekdays": [],
        },
    )
    work = Occurrence.objects.get(definition=definition)
    assert post_submit(c, h, work).status_code == 302
    work.refresh_from_db()
    assert post_review(c, h, work).status_code == 302
    definition.refresh_from_db()
    save_recurring(h, {"version": definition.version}, definition.pk, delete=True)
    env = dict(
        os.environ,
        DJANGO_SETTINGS_MODULE="config.settings.local",
        DB_NAME=connection.settings_dict["NAME"],
    )
    probe = f"import django; django.setup(); import json; from board.read_model import columns_for_household; from households.models import Household; w=columns_for_household(Household.objects.get(pk={h.pk}))[0].work; print(json.dumps([w.weekly_stars,w.all_time_stars,[x.title for x in w.completed_this_week]]))"
    for _ in range(2):
        result = subprocess.run(
            [sys.executable, "-c", probe],
            env=env,
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
        )
        assert json.loads(result.stdout.strip()) == [1, 1, ["Retained approval"]]
    c.logout()
    c.force_login(a)
    response = c.get(reverse("household_board", args=[h.pk]))
    assert response.context["columns"][0].work.all_time_stars == 1
    assert b"Retained approval" in response.content


@pytest.mark.django_db
def test_actual_foreign_history_totals_and_direct_reads_are_scoped():
    from allauth.account.models import EmailAddress
    from django.contrib.auth import get_user_model
    from django.test import Client

    from chores.review import submit_work
    from households.models import Child
    from households.services import create_household

    a, _, h, c, child, _ = ready()
    foreign_parent = get_user_model().objects.create_user(
        username="foreign-progress", email="foreign-progress@example.test"
    )
    EmailAddress.objects.create(
        user=foreign_parent, email=foreign_parent.email, verified=True
    )
    foreign = create_household(foreign_parent, "UTC")
    other_child = Child.objects.create(
        household=foreign, name="Private foreign child", pin_hash="PRIVATE-HASH"
    )
    work = save_one_off(
        foreign,
        {
            "title": "Private foreign completion",
            "child": other_child,
            "due_date": date(2026, 10, 25),
        },
    )
    instant = datetime.now(timezone.utc)
    submit_work(foreign, work.pk, work.version, other_child.pk, "UTC", instant)
    work.refresh_from_db()
    review_work(foreign, work.pk, work.version, foreign_parent, "approve", now=instant)
    response = c.get(
        reverse("household_board", args=[h.pk])
        + f"?child={other_child.pk}&household={foreign.pk}"
    )
    body = response.content.decode()
    assert response.context["columns"][0].work.all_time_stars == 0
    assert "Private foreign" not in body and "PRIVATE-HASH" not in body
    assert c.get(reverse("household_board", args=[foreign.pk])).status_code == 403
    outside = Client()
    outside.force_login(foreign_parent)
    assert outside.get(reverse("household_board", args=[h.pk])).status_code == 403
    assert columns_for_household(foreign)[0].work.all_time_stars == 1
