"""Submission authentication commits separately from the guarded state transition."""

from zoneinfo import ZoneInfo

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from households.models import Household
from households.services import Conflict

from .models import Approval, Definition, Occurrence
from .recurrence import complete_occurrence


def locked_work(household, occurrence_id, version, state):
    Household.objects.select_for_update().get(pk=household.pk)
    candidate = Occurrence.objects.filter(pk=occurrence_id, household=household).first()
    if not candidate:
        raise Conflict(
            "That chore is no longer available. The current board is shown below."
        )
    # Match the scheduler/edit/delete order, even for one-off definitions.
    Definition.objects.select_for_update().filter(pk=candidate.definition_id).first()
    work = Occurrence.objects.select_for_update().get(pk=candidate.pk)
    if work.version != version or work.state != state:
        raise Conflict(
            "That chore changed. The current board is shown below. Reopen it before trying again."
        )
    return work


@transaction.atomic
def submit_work(
    household, occurrence_id, version, child_id, browser_timezone, received_at
):
    work = locked_work(household, occurrence_id, version, "to_do")
    if work.child_id != child_id:
        raise Conflict("The assignment changed. Reopen it before trying again.")
    work.state = "awaiting_approval"
    work.submitted_at = received_at
    work.submitted_timezone = browser_timezone
    work.submitted_late = (
        received_at.astimezone(ZoneInfo(browser_timezone)).date() > work.due_date
    )
    work.version += 1
    work.save()
    Household.objects.filter(pk=household.pk).update(revision=F("revision") + 1)
    return work


@transaction.atomic
def review_work(household, occurrence_id, version, parent, action, note="", now=None):
    instant = now or timezone.now()
    work = locked_work(household, occurrence_id, version, "awaiting_approval")
    if action == "approve":
        work = complete_occurrence(household, work.pk, version, instant)
        Approval.objects.create(occurrence=work, parent=parent, approved_at=instant)
    elif action == "return" and note.strip():
        work.state = "to_do"
        work.return_note = note.strip()
        work.submitted_late = None
        work.version += 1
        work.save()
        Household.objects.filter(pk=household.pk).update(revision=F("revision") + 1)
    else:
        raise Conflict("A return needs an explanation.")
    return work
