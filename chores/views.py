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
