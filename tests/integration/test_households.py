import io
import logging
import re
import smtplib
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from urllib.parse import urlsplit

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, close_old_connections, transaction
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from households.models import Household, Invitation, Membership
from households.services import (
    Conflict,
    accept_invitation,
    create_household,
    token_digest,
)

PASSWORD = "Local-Synthetic-7392!"


def parent(email, verified=True):
    user = get_user_model().objects.create_user(
        username=email, email=email, password=PASSWORD
    )
    EmailAddress.objects.create(user=user, email=email, verified=verified, primary=True)
    return user


def unlock_fixture(client, user):
    from django.contrib.auth.hashers import make_password

    from households.models import ParentCredential
    from households.pins import encoded_pin

    membership = Membership.objects.filter(user=user).first()
    if membership:
        ParentCredential.objects.update_or_create(
            user=user,
            defaults={
                "pin_hash": make_password(encoded_pin("parent", user.pk, "2468")),
                "version": 1,
            },
        )
        assert (
            client.post(
                reverse("parent_unlock", args=[membership.household_id]),
                {"parent": user.pk, "pin": "2468"},
            ).status_code
            == 302
        )


def signed_in(user):
    client = Client()
    client.force_login(user)
    unlock_fixture(client, user)
    return client


def invite(owner, household, email):
    response = signed_in(owner).post(
        reverse("household_settings", args=[household.pk]), {"email": email}
    )
    assert response.status_code == 302
    path = next(
        urlsplit(url).path
        for url in re.findall(r"https?://[^\s]+", mail.outbox[-1].body)
        if "/households/invitations/" in url
    )
    token = path.rstrip("/").split("/")[-1]
    return Invitation.objects.get(token_hash=token_digest(token)), path


@pytest.mark.django_db
def test_create_and_intended_verified_join_equal_member_rights():
    first = parent("first@example.test")
    second = parent("second@example.test")
    client = signed_in(first)
    response = client.post(reverse("household_create"), {"timezone": "Europe/Warsaw"})
    assert response.status_code == 302
    household = Membership.objects.get(user=first).household
    invitation, path = invite(first, household, second.email)
    assert invitation.token_hash not in mail.outbox[-1].body
    recipient = signed_in(second)
    exchange = recipient.get(path)
    assert (
        exchange.status_code == 302
        and exchange.headers["Referrer-Policy"] == "no-referrer"
    )
    form = recipient.get(exchange.headers["Location"])
    assert form.status_code == 200 and form.headers["Referrer-Policy"] == "same-origin"
    assert "no-store" in form.headers["Cache-Control"]
    joined = recipient.post(exchange.headers["Location"])
    assert joined.status_code == 302
    invitation.refresh_from_db()
    assert invitation.consumed_at is not None
    assert household.memberships.count() == 2
    for member in (first, second):
        view = signed_in(member).get(reverse("household_settings", args=[household.pk]))
        assert (
            view.status_code == 200
            and first.email.encode() in view.content
            and second.email.encode() in view.content
        )
        assert (
            signed_in(member)
            .post(
                reverse("household_settings", args=[household.pk]),
                {"email": "third@example.test"},
            )
            .status_code
            == 409
        )
    assert recipient.get(path).status_code == 400
    assert recipient.post(exchange.headers["Location"]).status_code == 400


@pytest.mark.django_db
@pytest.mark.parametrize(
    "age,accepted", [(7 * 86400 - 1, True), (7 * 86400, False), (7 * 86400 + 1, False)]
)
def test_invitation_seven_day_boundary(age, accepted, monkeypatch):
    owner = parent("owner@example.test")
    target = parent("target@example.test")
    household = create_household(owner, "UTC")
    invitation, _ = invite(owner, household, target.email)
    now = timezone.now()
    invitation.expires_at = now + timedelta(seconds=7 * 86400 - age)
    invitation.save()
    monkeypatch.setattr("households.services.timezone.now", lambda: now)
    if accepted:
        assert accept_invitation(target, invitation.token_hash) == household
    else:
        with pytest.raises(PermissionDenied):
            accept_invitation(target, invitation.token_hash)
    assert Membership.objects.filter(user=target).exists() == accepted


@pytest.mark.django_db
def test_wrong_anonymous_unverified_tampered_and_reused_invitation_denied():
    owner = parent("owner@example.test")
    target = parent("target@example.test")
    wrong = parent("wrong@example.test")
    unverified = parent("unverified@example.test", False)
    household = create_household(owner, "UTC")
    wrong_household = create_household(wrong, "Pacific/Auckland")
    invitation, path = invite(owner, household, target.email)
    anonymous = Client()
    exchange = anonymous.get(path)
    assert exchange.status_code == 302 and exchange.headers["Location"].startswith(
        "/accounts/login/?next="
    )
    flow = reverse(
        "household_join", args=[anonymous.session["household_invitation_flow"]]
    )
    assert anonymous.post(flow).status_code == 403
    for user in (wrong, unverified):
        client = signed_in(user)
        next_path = client.get(path).headers["Location"]
        assert client.get(next_path).status_code == 403
        if user == wrong:
            assert client.get(reverse("household_entry")).headers[
                "Location"
            ] == reverse("household_board", args=[wrong_household.pk])
        next_path = client.get(path).headers["Location"]
        assert client.post(next_path).status_code == 403
    assert Client().get(path + "tampered").status_code == 404
    assert (
        signed_in(target).get("/households/invitations/malformed/").status_code == 400
    )
    invitation.refresh_from_db()
    assert invitation.consumed_at is None
    assert household.memberships.count() == 1


@pytest.mark.django_db
def test_actual_household_isolation_forged_ids_and_no_credential_exposure():
    first = parent("house-a@example.test")
    second = parent("house-b@example.test")
    outsider = parent("outsider@example.test")
    a = create_household(first, "Europe/Warsaw")
    b = create_household(second, "Pacific/Auckland")
    private, _ = invite(first, a, "private-recipient@example.test")
    for user in (second, outsider):
        client = signed_in(user)
        for target in (a.pk, 999999):
            url = reverse("household_settings", args=[target])
            response = client.get(url)
            assert response.status_code == 403
            assert b"private-recipient" not in response.content
            assert (
                client.post(
                    url,
                    {
                        "email": "forged@example.test",
                        "household_id": b.pk,
                        "invitation_id": private.pk,
                    },
                ).status_code
                == 403
            )
    assert a.invitations.count() == 1 and b.invitations.count() == 0
    content = signed_in(first).get(reverse("household_settings", args=[a.pk])).content
    assert (
        first.password.encode() not in content
        and private.token_hash.encode() not in content
    )
    assert second.email.encode() not in content and b"PIN_HASH" not in content


@pytest.mark.django_db
@pytest.mark.parametrize("zone", ["", "Not/A_timezone"])
def test_invalid_timezone_creates_no_partial_household(zone):
    user = parent("parent@example.test")
    assert (
        signed_in(user)
        .post(reverse("household_create"), {"timezone": zone})
        .status_code
        == 400
    )
    assert not Household.objects.exists() and not Membership.objects.exists()


@pytest.mark.django_db
def test_timezone_immutable_and_one_household_per_account():
    user = parent("parent@example.test")
    household = create_household(user, "Europe/Warsaw")
    client = signed_in(user)
    response = client.post(reverse("household_create"), {"timezone": "UTC"})
    assert response.status_code == 409 and Household.objects.count() == 1
    # Unknown settings input cannot create a timezone-changing operation.
    client.post(reverse("household_settings", args=[household.pk]), {"timezone": "UTC"})
    household.refresh_from_db()
    assert household.timezone == "Europe/Warsaw"
    household.timezone = "UTC"
    with pytest.raises(ValidationError):
        household.save()
    client.post("/accounts/logout/")
    client.force_login(user)
    unlock_fixture(client, user)
    assert (
        b"Europe/Warsaw"
        in client.get(reverse("household_settings", args=[household.pk])).content
    )


@pytest.mark.django_db
def test_expired_replacement_and_smtp_failure_are_atomic(monkeypatch):
    user = parent("owner@example.test")
    household = create_household(user, "UTC")
    old, old_path = invite(user, household, "second@example.test")
    old.expires_at = timezone.now() - timedelta(seconds=1)
    old.save()
    assert Client().get(old_path).status_code == 400

    def fail(*args, **kwargs):
        raise smtplib.SMTPException("private provider detail")

    with monkeypatch.context() as patch:
        patch.setattr("django.core.mail.message.EmailMessage.send", fail)
        response = signed_in(user).post(
            reverse("household_settings", args=[household.pk]),
            {"email": "second@example.test"},
        )
    assert response.status_code == 503 and b"private provider" not in response.content
    assert Invitation.objects.count() == 1
    old.refresh_from_db()
    assert old.superseded_at is None
    fresh, new_path = invite(user, household, "second@example.test")
    old.refresh_from_db()
    assert old.superseded_at is not None
    assert (
        Client().get(old_path).status_code == 400
        and Client().get(new_path).status_code == 302
    )
    assert fresh.available


@pytest.mark.django_db
def test_csrf_required_and_session_flow_is_not_transferable():
    user = parent("owner@example.test")
    target = parent("target@example.test")
    household = create_household(user, "UTC")
    _, path = invite(user, household, target.email)
    csrf = Client(enforce_csrf_checks=True)
    csrf.force_login(user)
    assert (
        csrf.post(reverse("household_create"), {"timezone": "UTC"}).status_code == 403
    )
    assert (
        csrf.post(
            reverse("household_settings", args=[household.pk]), {"email": target.email}
        ).status_code
        == 403
    )
    recipient = signed_in(target)
    flow = recipient.get(path).headers["Location"]
    assert signed_in(target).post(flow).status_code == 400
    csrf.force_login(target)
    csrf.get(path)
    private_flow = reverse(
        "household_join", args=[csrf.session["household_invitation_flow"]]
    )
    assert csrf.post(private_flow).status_code == 403


def race(actions):
    barrier = Barrier(len(actions))

    def run(action):
        close_old_connections()
        try:
            barrier.wait(timeout=10)
            try:
                action()
                return "accepted"
            except (Conflict, PermissionDenied):
                return "denied"
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=len(actions)) as pool:
        return list(pool.map(run, actions))


@pytest.mark.django_db(transaction=True)
def test_concurrent_acceptance_consumes_one_token_once():
    owner = parent("owner@example.test")
    target = parent("target@example.test")
    household = create_household(owner, "UTC")
    invitation, _ = invite(owner, household, target.email)
    outcomes = race([lambda: accept_invitation(target, invitation.token_hash)] * 2)
    assert (
        sorted(outcomes) == ["accepted", "denied"]
        and household.memberships.count() == 2
    )
    assert Membership.objects.filter(user=target).count() == 1


@pytest.mark.django_db(transaction=True)
def test_competing_invitations_cannot_take_third_parent_slot():
    owner = parent("owner@example.test")
    a = parent("a@example.test")
    b = parent("b@example.test")
    household = create_household(owner, "UTC")
    ia, _ = invite(owner, household, a.email)
    ib, _ = invite(owner, household, b.email)
    outcomes = race(
        [
            lambda: accept_invitation(a, ia.token_hash),
            lambda: accept_invitation(b, ib.token_hash),
        ]
    )
    assert (
        sorted(outcomes) == ["accepted", "denied"]
        and household.memberships.count() == 2
    )
    assert Invitation.objects.filter(consumed_at__isnull=False).count() == 1


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("compete", ["join", "create"])
def test_competing_join_or_create_cannot_give_account_two_households(compete):
    owner = parent("owner@example.test")
    other = parent("other@example.test")
    target = parent("target@example.test")
    a = create_household(owner, "UTC")
    b = create_household(other, "Europe/Warsaw")
    first, _ = invite(owner, a, target.email)
    second, _ = invite(other, b, target.email)
    competing = (
        (lambda: accept_invitation(target, second.token_hash))
        if compete == "join"
        else (lambda: create_household(target, "Pacific/Auckland"))
    )
    outcomes = race([lambda: accept_invitation(target, first.token_hash), competing])
    assert (
        sorted(outcomes) == ["accepted", "denied"]
        and Membership.objects.filter(user=target).count() == 1
    )
    assert Household.objects.count() == (
        2
        if compete == "join" or Membership.objects.get(user=target).household_id == a.pk
        else 3
    )


@pytest.mark.django_db
def test_database_constraints_bound_parent_slots():
    first = parent("first@example.test")
    second = parent("second@example.test")
    third = parent("third@example.test")
    household = create_household(first, "UTC")
    Membership.objects.create(user=second, household=household, slot=2)
    with pytest.raises(IntegrityError), transaction.atomic():
        Membership.objects.create(user=third, household=household, slot=3)
    with pytest.raises(IntegrityError), transaction.atomic():
        Membership.objects.create(user=third, household=household, slot=2)
    with pytest.raises(IntegrityError), transaction.atomic():
        Membership.objects.create(
            user=first, household=Household.objects.create(timezone="UTC"), slot=1
        )
    assert Household.objects.count() == 1 and household.memberships.count() == 2


def test_invitation_request_logs_redact_private_path_and_encoded_query():
    logger = logging.getLogger("django.server")
    handler = logger.handlers[0]
    stream = io.StringIO()
    previous = handler.stream
    handler.setStream(stream)
    try:
        logger.info(
            '"%s" %s',
            "GET /households/invitations/private-invite/?next=%2Fprivate-token HTTP/1.1",
            302,
        )
        logger.info('"%s" %s', "POST /households/join/private-flow/ HTTP/1.1", 302)
    finally:
        handler.setStream(previous)
    rendered = stream.getvalue()
    assert all(
        secret not in rendered
        for secret in ("private-invite", "private-token", "private-flow")
    )
    assert "[redacted]" in rendered


@pytest.mark.django_db
@pytest.mark.parametrize(
    "failure_path", ["create", "settings_render", "invite", "join"]
)
def test_household_domain_database_failures_are_private_recoverable_and_retryable(
    failure_path, monkeypatch, settings
):
    from django.db import OperationalError

    settings.DEBUG = True
    owner = parent("failure-owner@example.test")
    client = Client(raise_request_exception=False)
    client.force_login(owner)
    method, url, payload = (
        "post",
        reverse("household_create"),
        {"timezone": "Europe/Warsaw"},
    )
    household = None
    if failure_path != "create":
        household = create_household(owner, "Europe/Warsaw")
        url = reverse("household_settings", args=[household.pk])
        payload = {"email": "failure-recipient@example.test"}
        unlock_fixture(client, owner)
    if failure_path == "settings_render":
        method = "get"
    if failure_path == "join":
        target = parent("failure-recipient@example.test")
        _, private_path = invite(owner, household, target.email)
        client.force_login(target)
        url = client.get(private_path).headers["Location"]
        payload = {}

    marker = "synthetic-private-household-database-detail"

    def fail(*args, **kwargs):
        raise OperationalError(marker)

    before = (
        Household.objects.count(),
        Membership.objects.count(),
        Invitation.objects.count(),
        Invitation.objects.filter(consumed_at__isnull=False).count(),
    )
    stream = io.StringIO()
    handler = logging.getLogger("django.request").handlers[0]
    with monkeypatch.context() as patch:
        if failure_path == "create":
            patch.setattr("households.views.create_household", fail)
        elif failure_path == "settings_render":
            patch.setattr("households.views.render", fail)
        elif failure_path == "invite":

            class FailedMailAdapter:
                send_mail = staticmethod(fail)

            patch.setattr(
                "households.services.get_adapter",
                lambda *args, **kwargs: FailedMailAdapter(),
            )
        else:
            patch.setattr("households.views.accept_invitation", fail)
        previous = handler.stream
        handler.setStream(stream)
        try:
            response = getattr(client, method)(url, payload)
        finally:
            handler.setStream(previous)
    logged = stream.getvalue()
    exposed = marker.encode() in response.content or marker in logged
    assert not exposed
    assert response.status_code == 503
    assert b"Temporarily unavailable" in response.content
    assert b"Please try again shortly" in response.content
    assert "no-store" in response.headers["Cache-Control"]
    assert response.headers["Referrer-Policy"] == "same-origin"
    assert "Service Unavailable" in logged
    assert "Traceback" not in logged
    if failure_path == "join":
        assert url.rstrip("/").split("/")[-1] not in logged
    after = (
        Household.objects.count(),
        Membership.objects.count(),
        Invitation.objects.count(),
        Invitation.objects.filter(consumed_at__isnull=False).count(),
    )
    assert after == before
    # The unmodified input/current invitation can be retried after recovery.
    retry = getattr(client, method)(url, payload)
    assert retry.status_code == (200 if method == "get" else 302)
