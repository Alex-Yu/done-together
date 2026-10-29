import hashlib
import hmac
import re
from functools import wraps

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone

from accounts.adapter import AccountAdapter
from accounts.limits import authenticate_identity

from .models import BoardAuthority, Child, Membership, ParentCredential
from .services import household_for_parent


def encoded_pin(kind, identity, pin):
    return hmac.new(
        settings.PIN_HASH_PEPPER.encode(),
        f"{kind}:{identity}:{pin}".encode(),
        hashlib.sha256,
    ).hexdigest()


def validate_pin(pin):
    if not isinstance(pin, str) or not re.fullmatch(r"[0-9]{4}", pin):
        raise ValidationError("Enter exactly four digits, from 0 to 9.")


def member_parent(user, household_id, parent_id):
    household_for_parent(user, household_id)
    membership = (
        Membership.objects.select_related("user")
        .filter(household_id=household_id, user_id=parent_id)
        .first()
    )
    if (
        not membership
        or not membership.user.is_active
        or not EmailAddress.objects.filter(
            user=membership.user, email__iexact=membership.user.email, verified=True
        ).exists()
    ):
        raise PermissionDenied("That parent is unavailable.")
    return membership.user


def set_parent_pin(request, household_id, parent_id, password, pin):
    selected = member_parent(request.user, household_id, parent_id)
    validate_pin(pin)
    authenticated = AccountAdapter(request).authenticate(
        request, email=selected.email, password=password
    )
    if not authenticated or authenticated.pk != selected.pk:
        return False
    with transaction.atomic():
        # Serialize resets without bypassing shared password identity limits.
        type(selected).objects.select_for_update().get(pk=selected.pk)
        ParentCredential.objects.get_or_create(user=selected)
        credential = ParentCredential.objects.select_for_update().get(user=selected)
        credential.pin_hash = make_password(encoded_pin("parent", selected.pk, pin))
        credential.version += 1
        credential.save()
    return True


def verify_parent_pin(board_user, household_id, parent_id, pin):
    selected = member_parent(board_user, household_id, parent_id)
    credential = ParentCredential.objects.filter(user=selected).first()
    return authenticate_identity(
        "parent-pin",
        str(selected.pk),
        lambda: bool(
            credential
            and credential.pin_hash
            and isinstance(pin, str)
            and re.fullmatch(r"[0-9]{4}", pin)
            and check_password(
                encoded_pin("parent", selected.pk, pin), credential.pin_hash
            )
        ),
    )


def verify_child_pin(board_user, household_id, child_id, pin):
    household_for_parent(board_user, household_id)
    child = Child.objects.filter(household_id=household_id, pk=child_id).first()
    if not child:
        raise PermissionDenied("That child is unavailable.")
    return authenticate_identity(
        "child-pin",
        str(child.pk),
        lambda: bool(
            isinstance(pin, str)
            and re.fullmatch(r"[0-9]{4}", pin)
            and check_password(encoded_pin("child", child.pk, pin), child.pin_hash)
        ),
    )


def session_digest(request):
    if not request.session.session_key:
        request.session.save()
    return hmac.new(
        settings.PIN_HASH_PEPPER.encode(),
        ("board:" + request.session.session_key).encode(),
        hashlib.sha256,
    ).hexdigest()


def authority_valid(authority):
    if (
        not authority
        or (timezone.now() - authority.last_activity).total_seconds() >= 60
    ):
        return False
    credential = ParentCredential.objects.filter(
        user_id=authority.parent_id, version=authority.credential_version
    ).first()
    return bool(
        credential
        and credential.user.is_active
        and Membership.objects.filter(
            user_id=authority.parent_id, household_id=authority.household_id
        ).exists()
        and EmailAddress.objects.filter(
            user_id=authority.parent_id,
            verified=True,
            email__iexact=credential.user.email,
        ).exists()
    )


def authority_state(request, household_id):
    authority = BoardAuthority.objects.filter(
        session_hash=session_digest(request), household_id=household_id
    ).first()
    return authority if authority_valid(authority) else None


def unlock_parent(request, household_id, parent_id, pin):
    selected = member_parent(request.user, household_id, parent_id)
    with transaction.atomic():
        type(selected).objects.select_for_update().get(pk=selected.pk)
        credential = (
            ParentCredential.objects.select_for_update()
            .filter(user_id=parent_id)
            .first()
        )
        if not credential:
            authenticate_identity("parent-pin", str(parent_id), lambda: False)
            return False
        if not verify_parent_pin(request.user, household_id, parent_id, pin):
            return False
        BoardAuthority.objects.update_or_create(
            session_hash=session_digest(request),
            defaults={
                "household_id": household_id,
                "parent_id": parent_id,
                "credential_version": credential.version,
                "last_activity": timezone.now(),
            },
        )
    return True


def parent_unlocked_required(view):
    @wraps(view)
    def guarded(request, household_id, *args, **kwargs):
        household_for_parent(request.user, household_id)
        with transaction.atomic():
            authority = (
                BoardAuthority.objects.select_for_update()
                .filter(session_hash=session_digest(request), household_id=household_id)
                .first()
            )
            if not authority_valid(authority):
                if request.method == "GET":
                    return redirect("household_board", household_id=household_id)
                return HttpResponseForbidden(
                    "Parent controls are locked. Enter a parent PIN on the board."
                )
            request.parent_identity = authority.parent
            response = view(request, household_id, *args, **kwargs)
            if request.method == "POST" and response.status_code < 400:
                authority.last_activity = timezone.now()
                authority.save(update_fields=["last_activity"])
            return response

    return guarded


def save_child_pin(child, pin):
    validate_pin(pin)
    child.pin_hash = make_password(encoded_pin("child", child.pk, pin))
    child.save(update_fields=["pin_hash"])
