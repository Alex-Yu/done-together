import hashlib
import secrets
from datetime import timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from .models import Household, Invitation, Membership


class Conflict(Exception):
    pass


def require_verified(user):
    if (
        not user.is_authenticated
        or not EmailAddress.objects.filter(
            user=user, email__iexact=user.email, verified=True
        ).exists()
    ):
        raise PermissionDenied("A verified parent account is required.")


def household_for_parent(user, household_id):
    require_verified(user)
    membership = (
        Membership.objects.select_related("household")
        .filter(user=user, household_id=household_id)
        .first()
    )
    if not membership:
        raise PermissionDenied("This household is unavailable.")
    return membership.household


def token_digest(token):
    return hashlib.sha256(token.encode()).hexdigest()


def create_household(user, zone):
    require_verified(user)
    try:
        ZoneInfo(zone)
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        raise ValidationError("Choose a valid IANA scheduling timezone.") from None
    with transaction.atomic():
        get_user_model().objects.select_for_update().get(pk=user.pk)
        if Membership.objects.filter(user=user).exists():
            raise Conflict("Your account already belongs to a household.")
        household = Household.objects.create(timezone=zone)
        Membership.objects.create(user=user, household=household, slot=1)
        return household


def send_invitation(user, household_id, email, request):
    email = email.strip().lower()
    validate_email(email)
    household_for_parent(user, household_id)
    with transaction.atomic():
        household = Household.objects.select_for_update().get(pk=household_id)
        household_for_parent(user, household.pk)
        if household.memberships.count() >= 2:
            raise Conflict("This household already has two parents.")
        if household.memberships.filter(user__email__iexact=email).exists():
            raise ValidationError("That parent is already in this household.")
        now = timezone.now()
        token = secrets.token_urlsafe(32)
        Invitation.objects.filter(
            household=household,
            email=email,
            consumed_at__isnull=True,
            superseded_at__isnull=True,
        ).update(superseded_at=now)
        invitation = Invitation.objects.create(
            household=household,
            created_by=user,
            email=email,
            token_hash=token_digest(token),
            expires_at=now + timedelta(days=7),
        )
        path = reverse("household_invitation", args=[token])
        get_adapter(request).send_mail(
            "households/email/invitation",
            email,
            {"invitation_url": request.build_absolute_uri(path)},
        )
        return invitation


def invitation_for_recipient(user, digest):
    require_verified(user)
    invitation = (
        Invitation.objects.select_related("household").filter(token_hash=digest).first()
    )
    if (
        not invitation
        or not invitation.available
        or invitation.email.casefold() != user.email.casefold()
    ):
        raise PermissionDenied(
            "This invitation is invalid, expired, already used, or for another account."
        )
    return invitation


def accept_invitation(user, digest):
    require_verified(user)
    with transaction.atomic():
        get_user_model().objects.select_for_update().get(pk=user.pk)
        candidate = (
            Invitation.objects.only("household_id").filter(token_hash=digest).first()
        )
        if not candidate:
            raise PermissionDenied("This invitation is unavailable.")
        household = Household.objects.select_for_update().get(pk=candidate.household_id)
        invitation = Invitation.objects.select_for_update().get(token_hash=digest)
        if (
            not invitation.available
            or invitation.email.casefold() != user.email.casefold()
        ):
            raise PermissionDenied(
                "This invitation is invalid, expired, already used, or for another account."
            )
        if Membership.objects.filter(user=user).exists():
            raise Conflict("Your account already belongs to a household.")
        used_slots = set(household.memberships.values_list("slot", flat=True))
        if len(used_slots) >= 2:
            raise Conflict("This household already has two parents.")
        slot = next(slot for slot in (1, 2) if slot not in used_slots)
        Membership.objects.create(user=user, household=household, slot=slot)
        invitation.consumed_at = timezone.now()
        invitation.save(update_fields=["consumed_at"])
        household.revision += 1
        household.save(update_fields=["revision"])
        return household
