import secrets
from urllib.parse import urlencode

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods

from accounts.access import verified_parent_required
from accounts.adapter import EmailDeliveryError

from .forms import HouseholdForm, InvitationForm
from .models import Invitation, Membership
from .services import (
    Conflict,
    accept_invitation,
    create_household,
    household_for_parent,
    invitation_for_recipient,
    send_invitation,
    token_digest,
)


def pending_join_path(request):
    flow = request.session.get("household_invitation_flow")
    return reverse("household_join", args=[flow]) if flow else None


@require_GET
@verified_parent_required
def entry(request):
    if pending_join_path(request):
        return redirect(pending_join_path(request))
    membership = Membership.objects.filter(user=request.user).first()
    if membership:
        return redirect("household_settings", household_id=membership.household_id)
    return redirect("household_create")


@require_http_methods(["GET", "POST"])
@verified_parent_required
def create(request):
    form = HouseholdForm(request.POST or None)
    status = 200
    if request.method == "POST" and form.is_valid():
        try:
            household = create_household(request.user, form.cleaned_data["timezone"])
        except (ValidationError, Conflict) as error:
            form.add_error(None, str(error))
            status = 409 if isinstance(error, Conflict) else 400
        else:
            return redirect("household_settings", household_id=household.pk)
    elif request.method == "POST":
        status = 400
    return render(request, "households/create.html", {"form": form}, status=status)


@require_http_methods(["GET", "POST"])
@verified_parent_required
def settings(request, household_id):
    household = household_for_parent(request.user, household_id)
    form = InvitationForm(request.POST or None)
    status = 200
    sent = False
    if request.method == "POST" and form.is_valid():
        try:
            send_invitation(
                request.user, household.pk, form.cleaned_data["email"], request
            )
        except (ValidationError, Conflict, EmailDeliveryError) as error:
            form.add_error(
                None,
                "Email could not be sent. Please try again."
                if isinstance(error, EmailDeliveryError)
                else str(error),
            )
            status = (
                503
                if isinstance(error, EmailDeliveryError)
                else (409 if isinstance(error, Conflict) else 400)
            )
        else:
            messages.success(
                request, "Invitation email sent. The link expires in seven days."
            )
            return redirect("household_settings", household_id=household.pk)
    elif request.method == "POST":
        status = 400
    return render(
        request,
        "households/settings.html",
        {
            "household": household,
            "members": household.memberships.select_related("user"),
            "invitations": household.invitations.order_by("-created_at"),
            "form": form,
            "sent": sent,
        },
        status=status,
    )


@require_GET
def invitation(request, token):
    candidate = Invitation.objects.filter(token_hash=token_digest(token)).first()
    if not candidate or not candidate.available:
        return render(request, "households/invalid.html", status=400)
    flow = secrets.token_urlsafe(18)
    request.session["household_invitation_digest"] = candidate.token_hash
    request.session["household_invitation_flow"] = flow
    path = reverse("household_join", args=[flow])
    if not request.user.is_authenticated:
        return redirect(reverse("account_login") + "?" + urlencode({"next": path}))
    return redirect(path)


@require_http_methods(["GET", "POST"])
@verified_parent_required
def join(request, flow):
    if not secrets.compare_digest(
        flow, request.session.get("household_invitation_flow", "")
    ):
        return render(request, "households/invalid.html", status=400)
    digest = request.session.get("household_invitation_digest", "")
    try:
        candidate = invitation_for_recipient(request.user, digest)
        if request.method == "POST":
            household = accept_invitation(request.user, digest)
            request.session.pop("household_invitation_digest", None)
            request.session.pop("household_invitation_flow", None)
            return redirect("household_settings", household_id=household.pk)
    except (Conflict, PermissionDenied) as error:
        request.session.pop("household_invitation_digest", None)
        request.session.pop("household_invitation_flow", None)
        return render(
            request,
            "households/invalid.html",
            {"error": str(error)},
            status=409 if isinstance(error, Conflict) else 403,
        )
    return render(request, "households/join.html", {"household": candidate.household})
