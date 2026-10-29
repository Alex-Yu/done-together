"""Presentation contract. Work providers add persisted occurrences in005–008.

Production currently reads real scoped children and empty work. Tests may replace
load_visible_work internally; HTTP input never selects a fixture/provider.
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
    # No fake production work/awards. Future occurrence queries own visibility.
    return {}


def columns_for_household(household):
    work = load_visible_work(household)
    return tuple(
        Column(child.pk, child.name, work.get(child.pk, VisibleWork()))
        for child in household.children.order_by("pk")
    )
