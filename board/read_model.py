"""Household-scoped persisted active work; approval/week projection joins in008.

Tests can patch the work provider internally; HTTP never selects a fixture.
"""

from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum


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

    @property
    def items(self):
        return self.active + self.completed_this_week


@dataclass(frozen=True)
class Column:
    child_id: int
    name: str
    work: VisibleWork


def load_visible_work(household):
    from chores.models import Occurrence

    grouped = {}
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
                recurring=occurrence.definition_id is not None
                and occurrence.definition.schedule != "once",
            )
        )
    return {child: VisibleWork(active=tuple(cards)) for child, cards in grouped.items()}


def columns_for_household(household):
    work = load_visible_work(household)
    return tuple(
        Column(child.pk, child.name, work.get(child.pk, VisibleWork()))
        for child in household.children.order_by("pk")
    )
