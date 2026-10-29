"""Calendar recurrence shared by the independent scheduler and approval transaction."""

from datetime import timedelta
from zoneinfo import ZoneInfo

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from households.models import Household
from households.services import Conflict

from .models import Definition, Occurrence


def local_date(household, now=None):
    return (now or timezone.now()).astimezone(ZoneInfo(household.timezone)).date()


def scheduled(definition, day):
    return definition.schedule == "daily" or day.weekday() in definition.weekdays


def reconcile_locked(definition, today):
    """Caller holds household then definition locks; never acquire them after work."""
    if (
        Occurrence.objects.filter(definition=definition)
        .exclude(state="completed")
        .exists()
    ):
        return None
    for offset in range(7):
        day = today - timedelta(days=offset)
        if day < definition.eligible_from:
            break
        if scheduled(definition, day):
            if Occurrence.objects.filter(definition=definition, due_date=day).exists():
                return None
            work = Occurrence.objects.create(
                definition=definition,
                household_id=definition.household_id,
                title=definition.title,
                child_id=definition.child_id,
                due_date=day,
            )
            Household.objects.filter(pk=definition.household_id).update(
                revision=F("revision") + 1
            )
            return work
    return None


@transaction.atomic
def reconcile_definition(definition_id, now=None):
    candidate = Definition.objects.filter(
        pk=definition_id, schedule__in=["daily", "weekdays"]
    ).first()
    if not candidate:
        return None
    household = Household.objects.select_for_update().get(pk=candidate.household_id)
    definition = Definition.objects.select_for_update().filter(pk=definition_id).first()
    if not definition:
        return None
    return reconcile_locked(definition, local_date(household, now))


def reconcile_all(now=None):
    count = 0
    for identity in (
        Definition.objects.exclude(schedule="once")
        .values_list("pk", flat=True)
        .iterator()
    ):
        count += reconcile_definition(identity, now) is not None
    return count


@transaction.atomic
def save_recurring(household, data, definition_id=None, delete=False, now=None):
    Household.objects.select_for_update().get(pk=household.pk)
    if data.get("child") and data["child"].household_id != household.pk:
        raise PermissionDenied
    today = local_date(household, now)
    if definition_id is None:
        definition = Definition.objects.create(
            household=household,
            eligible_from=today,
            **{key: data[key] for key in ("title", "child", "schedule", "weekdays")},
        )
    else:
        definition = (
            Definition.objects.select_for_update()
            .filter(pk=definition_id, household=household)
            .exclude(schedule="once")
            .first()
        )
        if not definition:
            raise PermissionDenied("That schedule is unavailable.")
        if definition.version != data.get("version"):
            raise Conflict("This schedule changed. Reopen it before trying again.")
        if delete:
            # Lock current work only after its definition; completed snapshots survive SET_NULL.
            list(
                Occurrence.objects.select_for_update()
                .filter(definition=definition)
                .order_by("pk")
            )
            Occurrence.objects.filter(definition=definition).exclude(
                state="completed"
            ).delete()
            definition.delete()
        else:
            for key in ("title", "child", "schedule", "weekdays"):
                setattr(definition, key, data[key])
            definition.version += 1
            definition.save()
    if not delete:
        reconcile_locked(definition, today)
    Household.objects.filter(pk=household.pk).update(revision=F("revision") + 1)
    return definition


@transaction.atomic
def complete_occurrence(household, occurrence_id, version, now=None):
    """Atomic completion hook;007 adds guarded review/unique award in this transaction.

    No HTTP route exposes this boundary before child submission/review is implemented.
    """
    Household.objects.select_for_update().get(pk=household.pk)
    candidate = Occurrence.objects.filter(pk=occurrence_id, household=household).first()
    if not candidate:
        raise Conflict("That work is no longer available.")
    definition = (
        Definition.objects.select_for_update()
        .filter(pk=candidate.definition_id)
        .first()
    )
    work = Occurrence.objects.select_for_update().get(pk=candidate.pk)
    if work.state != "awaiting_approval" or work.version != version:
        raise Conflict("That work changed. Refresh before reviewing it.")
    work.state = "completed"
    work.completed_at = now or timezone.now()
    work.version += 1
    work.save()
    if definition and definition.schedule != "once":
        today = local_date(household, now)
        definition.eligible_from = max(definition.eligible_from, today)
        definition.save(update_fields=["eligible_from"])
        reconcile_locked(definition, today)
    Household.objects.filter(pk=household.pk).update(revision=F("revision") + 1)
    return work
