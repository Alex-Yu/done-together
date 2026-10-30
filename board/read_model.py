"""Household-scoped active work and approval-derived progress.

Tests can patch the work provider internally; HTTP never selects a fixture.
"""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import StrEnum
from zoneinfo import ZoneInfo

from django.utils import timezone


class State(StrEnum):
    TO_DO = "to_do"
    AWAITING = "awaiting_approval"
    COMPLETED = "completed"


@dataclass(frozen=True)
class Card:
    identity: str
    title: str
    state: State
    due_date: date
    persisted: bool = False
    recurring: bool = False
    overdue: bool = False
    completed_at: datetime | None = None
    submitted_late: bool | None = None
    return_note: str = ""

    @property
    def state_label(self):
        return {
            State.TO_DO: "To do",
            State.AWAITING: "Awaiting approval",
            State.COMPLETED: "Completed",
        }[self.state]


@dataclass(frozen=True)
class VisibleWork:
    active: tuple[Card, ...] = ()
    completed_this_week: tuple[Card, ...] = ()
    weekly_stars: int = 0
    all_time_stars: int = 0

    @property
    def items(self):
        return self.active + self.completed_this_week


@dataclass(frozen=True)
class Column:
    child_id: int
    name: str
    work: VisibleWork


def household_week(household, now):
    """Calendar Mondays, rather than a fixed 168-hour UTC duration."""
    zone = ZoneInfo(household.timezone)
    today = now.astimezone(zone).date()
    monday = today - timedelta(days=today.weekday())
    return (
        datetime.combine(monday, time.min, zone),
        datetime.combine(monday + timedelta(days=7), time.min, zone),
    )


def load_visible_work(household):
    from chores.models import Approval, Occurrence

    grouped = {}
    completed = {}
    totals = {}
    start, end = household_week(household, timezone.now())
    for approval in (
        Approval.objects.filter(occurrence__household=household)
        .select_related("occurrence")
        .order_by("approved_at", "pk")
    ):
        work = approval.occurrence
        totals[work.child_id] = totals.get(work.child_id, 0) + 1
        if start <= approval.approved_at < end:
            completed.setdefault(work.child_id, []).append(
                Card(
                    str(work.pk),
                    work.title,
                    State.COMPLETED,
                    work.due_date,
                    persisted=True,
                    completed_at=approval.approved_at,
                )
            )
    for occurrence in (
        Occurrence.objects.filter(household=household)
        .exclude(state="completed")
        .select_related("definition")
        .order_by("due_date", "pk")
    ):
        grouped.setdefault(occurrence.child_id, []).append(
            Card(
                str(occurrence.pk),
                occurrence.title,
                State(occurrence.state),
                occurrence.due_date,
                persisted=True,
                submitted_late=occurrence.submitted_late,
                return_note=occurrence.return_note,
                recurring=occurrence.definition_id is not None
                and occurrence.definition.schedule != "once",
            )
        )
    return {
        child: VisibleWork(
            active=tuple(grouped.get(child, ())),
            completed_this_week=tuple(completed.get(child, ())),
            weekly_stars=len(completed.get(child, ())),
            all_time_stars=totals.get(child, 0),
        )
        for child in grouped.keys() | totals.keys()
    }


def columns_for_household(household):
    work = load_visible_work(household)
    return tuple(
        Column(child.pk, child.name, work.get(child.pk, VisibleWork()))
        for child in household.children.order_by("pk")
    )
