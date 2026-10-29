from django import forms
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.access import verified_parent_required
from board.read_model import columns_for_household
from households.pin_views import parent_context
from households.pins import parent_unlocked_required
from households.services import Conflict, household_for_parent

from .forms import ChoreForm
from .models import Occurrence
from .services import save_one_off


@require_http_methods(["GET", "POST"])
@verified_parent_required
@parent_unlocked_required
def manage(request, household_id, occurrence_id=None, delete=False):
    household = household_for_parent(request.user, household_id)
    occurrence = None
    if occurrence_id:
        occurrence = Occurrence.objects.filter(
            pk=occurrence_id, household=household
        ).first()
        if not occurrence:
            raise PermissionDenied("That chore is unavailable.")
    initial = (
        {
            key: getattr(occurrence, key)
            for key in ("title", "child", "due_date", "version")
        }
        if occurrence
        else {}
    )
    form = ChoreForm(
        household, request.POST if request.method == "POST" else None, initial=initial
    )
    if delete:
        form = forms.Form(
            request.POST if request.method == "POST" else None,
            initial={"version": occurrence.version},
        )
        form.fields["version"] = forms.IntegerField(
            min_value=1, widget=forms.HiddenInput
        )
    status = 200
    if occurrence and occurrence.state != "to_do":
        form.full_clean()
        if not hasattr(form, "cleaned_data"):
            form.cleaned_data = {}
        form.add_error(
            None,
            "Only to-do chores can be edited or deleted. Awaiting work must first be returned; completed work is retained.",
        )
        status = 409
    elif request.method == "POST":
        if form.is_valid():
            try:
                save_one_off(household, form.cleaned_data, occurrence_id, delete)
            except Conflict as error:
                form.add_error(None, str(error))
                status = 409
            except DatabaseError:
                form.add_error(
                    None,
                    "Unable to save. Return to the board to check the current result before retrying.",
                )
                status = 503
            else:
                messages.success(
                    request, "Chore deleted." if delete else "Chore saved."
                )
                return redirect("household_board", household_id=household.pk)
        else:
            status = 400
    return render(
        request,
        "chores/form.html",
        parent_context(request, household)
        | {
            "form": form,
            "heading": "Delete chore"
            if delete
            else ("Edit chore" if occurrence else "Assign one-off chore"),
            "delete": delete,
            "occurrence": occurrence,
            "columns": columns_for_household(household) if status == 409 else (),
        },
        status=status,
    )


@require_http_methods(["GET", "POST"])
@verified_parent_required
@parent_unlocked_required
def recurring(request, household_id, definition_id=None, delete=False):
    from .forms import RecurringForm
    from .models import Definition
    from .recurrence import save_recurring

    household = household_for_parent(request.user, household_id)
    definition = None
    if definition_id:
        definition = (
            Definition.objects.filter(pk=definition_id, household=household)
            .exclude(schedule="once")
            .first()
        )
        if not definition:
            raise PermissionDenied("That schedule is unavailable.")
    initial = (
        {
            key: getattr(definition, key)
            for key in ("title", "child", "schedule", "weekdays", "version")
        }
        if definition
        else {}
    )
    form = RecurringForm(
        household, request.POST if request.method == "POST" else None, initial=initial
    )
    if delete:
        form = forms.Form(
            request.POST if request.method == "POST" else None,
            initial={"version": definition.version},
        )
        form.fields["version"] = forms.IntegerField(
            min_value=1, widget=forms.HiddenInput
        )
    status = 200
    if request.method == "POST":
        if form.is_valid():
            try:
                save_recurring(household, form.cleaned_data, definition_id, delete)
            except Conflict as error:
                form.add_error(None, str(error))
                status = 409
            except DatabaseError:
                form.add_error(
                    None,
                    "Unable to save. Return to the board to check the current result before retrying.",
                )
                status = 503
            else:
                messages.success(
                    request,
                    "Schedule deleted."
                    if delete
                    else "Schedule saved. Current work keeps its captured details.",
                )
                return redirect("household_board", household_id=household.pk)
        else:
            status = 400
    return render(
        request,
        "chores/recurring.html",
        parent_context(request, household)
        | {
            "form": form,
            "definition": definition,
            "delete": delete,
            "heading": "Delete recurring chore"
            if delete
            else ("Edit recurring chore" if definition else "Assign recurring chore"),
        },
        status=status,
    )


def transition_page(request, household_id, occurrence_id, reviewing=False):
    from django.utils import timezone

    from households.pins import verify_child_pin

    from .forms import ReviewForm, SubmissionForm
    from .review import review_work, submit_work

    received_at = timezone.now()
    household = household_for_parent(request.user, household_id)
    occurrence = (
        Occurrence.objects.filter(pk=occurrence_id, household=household)
        .select_related("child")
        .first()
    )
    if not occurrence:
        if request.method == "GET":
            raise PermissionDenied("That chore is unavailable.")
        from households.pin_views import ParentForm

        messages.error(
            request,
            "That chore is unavailable or changed. Check the current board before trying again.",
        )
        return render(
            request,
            "households/board.html",
            parent_context(request, household)
            | {
                "columns": columns_for_household(household),
                "unlock_form": ParentForm(
                    household, initial={"parent": request.user.pk}
                ),
            },
            status=409,
        )
    form = (ReviewForm if reviewing else SubmissionForm)(
        request.POST if request.method == "POST" else None,
        initial={"version": occurrence.version},
    )
    status = 200
    if request.method == "POST":
        if form.is_valid():
            # Do not enclose child authentication in a transition transaction: a
            # stale/deleted/state-denied action must not roll back failure counts.
            authenticated = reviewing or verify_child_pin(
                request.user,
                household.pk,
                occurrence.child_id,
                form.cleaned_data["pin"],
            )
            if not authenticated:
                form.add_error(
                    None,
                    "Unable to submit. Use the assigned child’s PIN or try again in five minutes.",
                )
                status = 400
            else:
                try:
                    if reviewing:
                        review_work(
                            household,
                            occurrence.pk,
                            form.cleaned_data["version"],
                            request.parent_identity,
                            form.cleaned_data["action"],
                            form.cleaned_data["note"],
                        )
                    else:
                        submit_work(
                            household,
                            occurrence.pk,
                            form.cleaned_data["version"],
                            occurrence.child_id,
                            form.cleaned_data["browser_timezone"],
                            received_at,
                        )
                except Conflict as error:
                    form.add_error(None, str(error))
                    status = 409
                except DatabaseError:
                    form.add_error(
                        None,
                        "Unable to confirm the result. Check the board before retrying.",
                    )
                    status = 503
                else:
                    messages.success(
                        request,
                        (
                            "Chore approved. One star earned."
                            if form.cleaned_data["action"] == "approve"
                            else "Chore returned with your explanation."
                        )
                        if reviewing
                        else "Chore submitted for approval.",
                    )
                    return redirect("household_board", household_id=household.pk)
        else:
            status = 400
    return render(
        request,
        "chores/transition.html",
        parent_context(request, household)
        | {
            "form": form,
            "occurrence": occurrence,
            "reviewing": reviewing,
            "heading": "Review chore" if reviewing else "Submit chore",
            "columns": columns_for_household(household) if status == 409 else (),
        },
        status=status,
    )


@require_http_methods(["GET", "POST"])
@verified_parent_required
def submit(request, household_id, occurrence_id):
    return transition_page(request, household_id, occurrence_id)


@require_http_methods(["GET", "POST"])
@verified_parent_required
@parent_unlocked_required
def review(request, household_id, occurrence_id):
    return transition_page(request, household_id, occurrence_id, reviewing=True)
