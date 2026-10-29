from django import forms
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from accounts.access import verified_parent_required

from .models import BoardAuthority, Child
from .pins import (
    authority_state,
    parent_unlocked_required,
    save_child_pin,
    session_digest,
    set_parent_pin,
    unlock_parent,
)
from .services import household_for_parent


def pin_field(label):
    return forms.RegexField(
        r"\A[0-9]{4}\Z",
        label=label,
        strip=False,
        widget=forms.PasswordInput(
            attrs={"inputmode": "numeric", "pattern": "[0-9]{4}", "autocomplete": "off"}
        ),
    )


class ParentForm(forms.Form):
    parent = forms.ChoiceField(label="Parent")
    pin = pin_field("Parent PIN")

    def __init__(self, household, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].choices = [
            (member.user_id, member.user.email)
            for member in household.memberships.select_related("user")
        ]


class ParentSetupForm(ParentForm):
    password = forms.CharField(
        label="Selected parent’s account password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    pin = pin_field("New parent PIN")


class ChildForm(forms.Form):
    name = forms.CharField(label="Child display name")
    pin = pin_field("Child PIN")


class ChildNameForm(forms.Form):
    name = forms.CharField(label="Child display name")


class ChildPinForm(forms.Form):
    pin = pin_field("New child PIN")


def parent_context(request, household):
    authority = authority_state(request, household.pk)
    return {
        "household": household,
        "parent_authority": authority,
        "parent_remaining": max(
            0, 60 - (timezone.now() - authority.last_activity).total_seconds()
        )
        if authority
        else 0,
        "parent_activity_url": reverse("parent_activity", args=[household.pk]),
        "parent_board_url": reverse("household_board", args=[household.pk]),
    }


@require_GET
@verified_parent_required
def board(request, household_id):
    household = household_for_parent(request.user, household_id)
    return render(
        request,
        "households/board.html",
        parent_context(request, household)
        | {
            "unlock_form": ParentForm(household, initial={"parent": request.user.pk}),
            "children": household.children.all(),
        },
    )


@require_POST
@verified_parent_required
def unlock(request, household_id):
    household = household_for_parent(request.user, household_id)
    form = ParentForm(household, request.POST)
    if form.is_valid() and unlock_parent(
        request,
        household_id,
        int(form.cleaned_data["parent"]),
        form.cleaned_data["pin"],
    ):
        return redirect("household_board", household_id=household_id)
    if form.is_valid():
        form.add_error(
            None,
            "Unable to unlock. Check the selected parent and PIN or try again in five minutes.",
        )
    return render(
        request,
        "households/board.html",
        parent_context(request, household)
        | {"unlock_form": form, "children": household.children.all()},
        status=400,
    )


@require_POST
@verified_parent_required
def lock(request, household_id):
    household_for_parent(request.user, household_id)
    BoardAuthority.objects.filter(
        session_hash=session_digest(request), household_id=household_id
    ).delete()
    return redirect("household_board", household_id=household_id)


@require_POST
@verified_parent_required
@parent_unlocked_required
def activity(request, household_id):
    return JsonResponse({"remaining_seconds": 60})


@require_http_methods(["GET", "POST"])
@verified_parent_required
def parent_pin(request, household_id):
    household = household_for_parent(request.user, household_id)
    form = ParentSetupForm(
        household, request.POST or None, initial={"parent": request.user.pk}
    )
    if request.method == "POST" and form.is_valid():
        if set_parent_pin(
            request,
            household_id,
            int(form.cleaned_data["parent"]),
            form.cleaned_data["password"],
            form.cleaned_data["pin"],
        ):
            messages.success(
                request, "Parent PIN updated. Enter the new PIN to unlock controls."
            )
            return redirect("household_board", household_id=household_id)
        form.add_error(
            None,
            "Unable to verify that parent’s password. Check the details or try again in five minutes.",
        )
    return render(
        request,
        "households/parent_pin.html",
        {"household": household, "form": form},
        status=400 if request.method == "POST" else 200,
    )


@require_http_methods(["GET", "POST"])
@verified_parent_required
@parent_unlocked_required
def child_create(request, household_id):
    household = household_for_parent(request.user, household_id)
    form = ChildForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            child = Child.objects.create(
                household=household, name=form.cleaned_data["name"], pin_hash=""
            )
            save_child_pin(child, form.cleaned_data["pin"])
            household.revision += 1
            household.save(update_fields=["revision"])
        return redirect("household_settings", household_id=household_id)
    return render(
        request,
        "households/child_form.html",
        parent_context(request, household) | {"form": form, "heading": "Add child"},
        status=400 if request.method == "POST" else 200,
    )


@require_http_methods(["GET", "POST"])
@verified_parent_required
@parent_unlocked_required
def child_edit(request, household_id, child_id, pin=False):
    from django.core.exceptions import PermissionDenied

    household = household_for_parent(request.user, household_id)
    child = Child.objects.filter(household=household, pk=child_id).first()
    if not child:
        raise PermissionDenied("That child is unavailable.")
    form = (ChildPinForm if pin else ChildNameForm)(
        request.POST or None, initial={} if pin else {"name": child.name}
    )
    if request.method == "POST" and form.is_valid():
        if pin:
            save_child_pin(child, form.cleaned_data["pin"])
        else:
            child.name = form.cleaned_data["name"]
            child.save(update_fields=["name"])
        household.revision += 1
        household.save(update_fields=["revision"])
        return redirect("household_settings", household_id=household_id)
    return render(
        request,
        "households/child_form.html",
        parent_context(request, household)
        | {"form": form, "heading": "Reset child PIN" if pin else "Edit child name"},
        status=400 if request.method == "POST" else 200,
    )
