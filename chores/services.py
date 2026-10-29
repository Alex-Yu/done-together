from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F

from households.models import Household
from households.services import Conflict

from .models import Definition, Occurrence


@transaction.atomic
def save_one_off(household, data, occurrence_id=None, delete=False):
    # Household serializes board-affecting writes; definition precedes occurrence.
    Household.objects.select_for_update().get(pk=household.pk)
    if data.get("child") and data["child"].household_id != household.pk:
        raise PermissionDenied
    if occurrence_id is None:
        definition = Definition.objects.create(
            household=household,
            **{key: data[key] for key in ("title", "child", "due_date")},
        )
        occurrence = Occurrence.objects.create(
            definition=definition,
            household=household,
            title=definition.title,
            child=definition.child,
            due_date=definition.due_date,
        )
    else:
        candidate = Occurrence.objects.filter(
            pk=occurrence_id, household=household
        ).first()
        if not candidate:
            raise PermissionDenied("That chore is unavailable.")
        definition = (
            Definition.objects.select_for_update()
            .filter(pk=candidate.definition_id, household=household)
            .first()
        )
        occurrence = Occurrence.objects.select_for_update().get(pk=candidate.pk)
        if (
            not definition
            or definition.schedule != "once"
            or occurrence.state != "to_do"
            or occurrence.version != data.get("version")
        ):
            raise Conflict(
                "This chore changed or cannot be changed in its current state. The current board is shown below. Reopen the chore before trying again."
            )
        if delete:
            occurrence.delete()
            definition.delete()
        else:
            for key in ("title", "child", "due_date"):
                setattr(definition, key, data[key])
                setattr(occurrence, key, data[key])
            definition.save()
            occurrence.version += 1
            occurrence.save()
    Household.objects.filter(pk=household.pk).update(revision=F("revision") + 1)
    return occurrence
