import io
import json
import logging
import os
import re
import smtplib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from datetime import timezone as dt_timezone
from threading import Barrier
from urllib.parse import urlsplit

import pytest
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.utils import user_pk_to_url_str
from django.contrib.auth import get_user_model
from django.core import mail
from django.db import close_old_connections
from django.test import Client, override_settings
from django.urls import reverse
from django.utils import timezone

from accounts.limits import private_key
from accounts.models import AuthenticationLimit, RequestLimit
from accounts.tokens import OneHourResetTokenGenerator

PASSWORD = "River-Cloud-4829!"
NEW_PASSWORD = "Amber-Mountain-4932!"


@pytest.fixture
def make_user(db):
    def create(email="parent@example.test", verified=True):
        user = get_user_model().objects.create_user(
            username=email, email=email, password=PASSWORD
        )
        EmailAddress.objects.create(
            user=user, email=email, verified=verified, primary=True
        )
        return user

    return create


def captured_path(fragment):
    matches = re.findall(r"https?://[^\s]+", mail.outbox[-1].body)
    return next(urlsplit(url).path for url in matches if fragment in url)


def login(client, email="parent@example.test", password=PASSWORD):
    return client.post("/accounts/login/", {"login": email, "password": password})


@pytest.mark.django_db
def test_registration_verification_signin_signout_and_private_headers(client):
    response = client.post(
        "/accounts/signup/",
        {"email": "Parent@Example.test", "password1": PASSWORD, "password2": PASSWORD},
    )
    assert response.status_code == 302
    user = get_user_model().objects.get(email="parent@example.test")
    assert user.password.startswith("argon2$") and user.check_password(PASSWORD)
    assert not EmailAddress.objects.get(user=user).verified
    path = captured_path("confirm-email/")
    response = client.get(path)
    assert response.status_code == 302
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert "no-store" in response.headers["Cache-Control"]
    safe_path = response.headers["Location"]
    assert safe_path.startswith("/accounts/verification/confirm/")
    assert path not in safe_path
    form_page = client.get(safe_path)
    assert form_page.headers["Referrer-Policy"] == "same-origin"
    assert client.post(safe_path).status_code == 302
    assert client.post(path).status_code == 404
    assert login(client).status_code == 302
    assert client.session["_auth_user_id"] == str(user.pk)
    assert client.get("/").status_code == 200
    assert client.post("/accounts/logout/").status_code == 302
    assert "_auth_user_id" not in client.session
    assert get_user_model().objects.get(pk=user.pk).check_password(PASSWORD)


@pytest.mark.django_db
@pytest.mark.parametrize("age,valid", [(3599, True), (3600, False), (3601, False)])
def test_verification_exact_one_hour_boundary(make_user, client, age, valid):
    user = make_user(verified=False)
    address = EmailAddress.objects.get(user=user)
    confirmation = EmailConfirmation.create(address)
    confirmation.sent = timezone.now() - timedelta(seconds=age)
    confirmation.save()
    path = reverse("account_confirm_email", args=[confirmation.key])
    response = client.post(path)
    assert response.status_code == (302 if valid else 404)
    address.refresh_from_db()
    assert address.verified == valid


@pytest.mark.django_db
def test_tampered_verification_and_duplicate_registration_are_recoverable(
    make_user, client
):
    make_user()
    response = client.post(
        "/accounts/signup/",
        {"email": "parent@example.test", "password1": PASSWORD, "password2": PASSWORD},
        follow=True,
    )
    assert response.status_code == 200
    assert get_user_model().objects.count() == 1
    assert b"already exists" not in response.content.lower()
    response = client.post("/accounts/confirm-email/malformed-token/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_recovery_replaces_password_and_cannot_replay(make_user, client):
    user = make_user()
    assert (
        client.post("/accounts/password/reset/", {"email": user.email}).status_code
        == 302
    )
    path = captured_path("password/reset/key/")
    response = client.get(path)
    assert response.status_code == 302
    safe_path = response.headers["Location"]
    assert "set-password" in safe_path
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert "no-store" in response.headers["Cache-Control"]
    response = client.post(
        safe_path, {"password1": NEW_PASSWORD, "password2": NEW_PASSWORD}
    )
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.check_password(NEW_PASSWORD) and not user.check_password(PASSWORD)
    assert b"invalid, expired or already used" in client.get(path).content
    assert login(Client(), password=PASSWORD).status_code == 200
    assert login(Client(), password=NEW_PASSWORD).status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize("age,valid", [(3599, True), (3600, False), (3601, False)])
def test_recovery_exact_one_hour_and_tamper_boundary(
    make_user, monkeypatch, client, age, valid
):
    user = make_user()
    clock = datetime(2026, 10, 28, 12, 0, 0)
    monkeypatch.setattr(OneHourResetTokenGenerator, "_now", lambda self: clock)
    generator = OneHourResetTokenGenerator()
    token = generator.make_token(user)
    assert not generator.check_token(user, token + "tampered")
    clock += timedelta(seconds=age)
    assert generator.check_token(user, token) is valid
    path = reverse(
        "account_reset_password_from_key",
        kwargs={"uidb36": user_pk_to_url_str(user), "key": token},
    )
    response = client.get(path)
    assert response.status_code == (302 if valid else 200)
    if not valid:
        assert b"invalid, expired or already used" in response.content
    user.set_password(NEW_PASSWORD)
    user.save()
    assert not generator.check_token(user, token)


@pytest.mark.django_db
def test_unknown_and_known_recovery_have_same_response_and_delivery_failure(
    make_user, client, monkeypatch
):
    make_user()
    known = client.post("/accounts/password/reset/", {"email": "parent@example.test"})
    unknown = client.post(
        "/accounts/password/reset/", {"email": "unknown@example.test"}
    )
    assert (known.status_code, known.headers["Location"]) == (
        unknown.status_code,
        unknown.headers["Location"],
    )

    def fail(*args, **kwargs):
        raise smtplib.SMTPException("private SMTP details must not appear")

    monkeypatch.setattr("django.core.mail.message.EmailMessage.send", fail)
    for email in ("parent@example.test", "unknown@example.test"):
        response = client.post("/accounts/password/reset/", {"email": email})
        assert response.status_code == 503
        assert b"Email could not be sent" in response.content
        assert b"private SMTP" not in response.content
        assert "no-store" in response.headers["Cache-Control"]


@pytest.mark.django_db
def test_failed_registration_email_can_be_retried_without_duplicate_account(
    client, monkeypatch
):
    def fail(*args, **kwargs):
        raise OSError("private provider password detail")

    with monkeypatch.context() as patch:
        patch.setattr("django.core.mail.message.EmailMessage.send", fail)
        response = client.post(
            "/accounts/signup/",
            {
                "email": "retry@example.test",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
    assert response.status_code == 503
    user = get_user_model().objects.get(email="retry@example.test")
    assert not EmailAddress.objects.get(user=user).verified
    unsent = EmailConfirmation.objects.get(email_address__user=user)
    assert unsent.sent is None
    unsent_path = reverse("account_confirm_email", args=[unsent.key])
    assert client.get(unsent_path).status_code == 400
    assert client.post(unsent_path).status_code == 404
    assert b"private provider" not in response.content
    assert (
        client.post("/accounts/verification/resend/", {"email": user.email}).status_code
        == 200
    )
    assert client.post(captured_path("confirm-email/")).status_code == 302
    assert get_user_model().objects.count() == 1
    assert login(client, email=user.email).status_code == 302


@pytest.mark.django_db
@override_settings(ROOT_URLCONF="tests.integration.account_guard_urls")
def test_verified_guard_direct_requests_and_unverified_signin(make_user):
    client = Client()
    assert client.get("/_test/protected/").status_code == 403
    user = make_user(verified=False)
    login(client)
    assert "_auth_user_id" not in client.session
    client.force_login(user)
    assert client.get("/_test/protected/").status_code == 403
    EmailAddress.objects.filter(user=user).update(verified=True)
    assert client.get("/_test/protected/").status_code == 200
    assert client.post("/accounts/logout/").status_code == 302
    assert client.get("/_test/protected/").status_code == 403


@pytest.mark.django_db
def test_five_failures_restrict_correct_password_until_exact_expiry_without_extension(
    make_user, monkeypatch
):
    make_user()
    clock = datetime(2026, 10, 28, 12, 0, tzinfo=dt_timezone.utc)
    monkeypatch.setattr("accounts.limits.timezone.now", lambda: clock)
    for _ in range(4):
        assert login(Client(), password="incorrect").status_code == 200
    limit = AuthenticationLimit.objects.get(
        key=private_key("password", "parent@example.test")
    )
    assert limit.failures == 4 and limit.blocked_until is None
    assert login(Client(), password="incorrect").status_code == 200
    limit.refresh_from_db()
    deadline = limit.blocked_until
    assert deadline == clock + timedelta(minutes=5)
    restricted = Client()
    assert (
        login(restricted).status_code == 200
        and "_auth_user_id" not in restricted.session
    )
    clock += timedelta(seconds=299)
    login(Client(), password="incorrect")
    limit.refresh_from_db()
    assert limit.failures == 5 and limit.blocked_until == deadline
    clock += timedelta(seconds=1)
    assert login(Client()).status_code == 302
    limit.refresh_from_db()
    assert limit.failures == 0 and limit.blocked_until is None


@pytest.mark.django_db
def test_permitted_success_clears_consecutive_failures(make_user):
    make_user()
    for _ in range(4):
        login(Client(), password="incorrect")
    assert login(Client()).status_code == 302
    login(Client(), password="incorrect")
    limit = AuthenticationLimit.objects.get(
        key=private_key("password", "parent@example.test")
    )
    assert limit.failures == 1 and limit.blocked_until is None


@pytest.mark.django_db(transaction=True)
def test_concurrent_independent_sessions_do_not_lose_failures():
    user = get_user_model().objects.create_user(
        username="parallel", email="parallel@example.test", password=PASSWORD
    )
    EmailAddress.objects.create(
        user=user, email=user.email, verified=True, primary=True
    )
    barrier = Barrier(5)

    def attempt(number):
        close_old_connections()
        try:
            barrier.wait(timeout=10)
            return (
                Client(REMOTE_ADDR=f"127.0.0.{number + 2}")
                .post(
                    "/accounts/login/", {"login": user.email, "password": "incorrect"}
                )
                .status_code
            )
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=5) as pool:
        assert list(pool.map(attempt, range(5))) == [200] * 5
    limit = AuthenticationLimit.objects.get(key=private_key("password", user.email))
    assert limit.failures == 5 and limit.blocked_until is not None


@pytest.mark.django_db(transaction=True)
def test_failure_counters_are_shared_with_an_independent_process(settings):
    user = get_user_model().objects.create_user(
        username="process", email="process@example.test", password=PASSWORD
    )
    EmailAddress.objects.create(
        user=user, email=user.email, verified=True, primary=True
    )
    for _ in range(2):
        login(Client(), email=user.email, password="incorrect")
    script = """import django,json,sys; django.setup(); from django.test import Client; data=json.load(sys.stdin); results=[Client(HTTP_HOST='127.0.0.1').post('/accounts/login/',data).status_code for _ in range(3)]; print(results)"""
    env = os.environ | {
        "DJANGO_SETTINGS_MODULE": "config.settings.local",
        "DB_NAME": settings.DATABASES["default"]["NAME"],
    }
    result = subprocess.run(
        [sys.executable, "-c", script],
        input=json.dumps({"login": user.email, "password": "incorrect"}),
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "[200, 200, 200]"
    limit = AuthenticationLimit.objects.get(key=private_key("password", user.email))
    assert limit.failures == 5 and limit.blocked_until is not None


@pytest.mark.django_db
def test_source_throttle_is_separate_and_recoverable(client, monkeypatch):
    clock = timezone.now()
    monkeypatch.setattr("accounts.limits.timezone.now", lambda: clock)
    RequestLimit.objects.create(
        key=private_key("account-request-source", "127.0.0.1"),
        count=60,
        window_started=clock,
    )
    response = login(client, email="unknown@example.test", password="incorrect")
    assert response.status_code == 429 and response.headers["Retry-After"] == "60"
    assert not AuthenticationLimit.objects.exists()
    clock += timedelta(seconds=60)
    assert (
        login(client, email="unknown@example.test", password="incorrect").status_code
        == 200
    )


@pytest.mark.django_db
def test_credentials_not_echoed_csrf_and_cookie_safety(client, settings):
    csrf_client = Client(enforce_csrf_checks=True)
    for path in (
        "/accounts/login/",
        "/accounts/signup/",
        "/accounts/password/reset/",
        "/accounts/verification/resend/",
        "/accounts/logout/",
    ):
        assert csrf_client.post(path).status_code == 403
    response = login(client, password="do-not-echo-secret")
    assert b"do-not-echo-secret" not in response.content
    assert settings.SESSION_COOKIE_HTTPONLY
    assert settings.SECURE_REFERRER_POLICY == "same-origin"
    assert settings.AUTHENTICATION_BACKENDS == [
        "allauth.account.auth_backends.AuthenticationBackend"
    ]


def test_routine_request_logs_redact_path_and_query_tokens():
    stream = io.StringIO()
    logger = logging.getLogger("django.server")
    handler = logger.handlers[0]
    previous = handler.stream
    handler.setStream(stream)
    try:
        logger.info(
            '"%s" %s %s',
            "GET /accounts/password/reset/key/uid-private-secret/?next=%2Faccounts%2Fconfirm-email%2Fsecond-secret%2F&token=third-secret HTTP/1.1",
            200,
            42,
        )
        logger.info(
            '"%s" %s %s', "GET /accounts/confirm-email/fourth-secret/ HTTP/1.1", 200, 42
        )
    finally:
        handler.setStream(previous)
    security = logging.getLogger("django.security")
    handler = security.handlers[0]
    previous = handler.stream
    handler.setStream(stream)
    try:
        logging.getLogger("django.security.csrf").warning(
            "Forbidden: %s", "/accounts/confirm-email/fifth-secret/"
        )
    finally:
        handler.setStream(previous)
    text = stream.getvalue()
    assert all(
        secret not in text
        for secret in (
            "private-secret",
            "second-secret",
            "third-secret",
            "fourth-secret",
            "fifth-secret",
        )
    )
    assert "[redacted]" in text and "200 42" in text


@pytest.mark.django_db
def test_second_verification_link_invalidates_previous_session_flow(make_user, client):
    first = EmailConfirmation.create(
        EmailAddress.objects.get(user=make_user("first@example.test", verified=False))
    )
    second = EmailConfirmation.create(
        EmailAddress.objects.get(user=make_user("second@example.test", verified=False))
    )
    for confirmation in (first, second):
        confirmation.sent = timezone.now()
        confirmation.save()
    old_flow = client.get(reverse("account_confirm_email", args=[first.key])).headers[
        "Location"
    ]
    current_flow = client.get(
        reverse("account_confirm_email", args=[second.key])
    ).headers["Location"]
    assert client.post(old_flow).status_code == 400
    assert not EmailAddress.objects.get(user=first.email_address.user).verified
    assert client.post(current_flow).status_code == 302
    assert EmailAddress.objects.get(user=second.email_address.user).verified


@pytest.mark.django_db
def test_account_database_failure_is_recoverable_without_private_details(
    client, monkeypatch
):
    from django.db import OperationalError

    def fail(*args, **kwargs):
        raise OperationalError("private connection parameters must not escape")

    monkeypatch.setattr("accounts.middleware.allow_source", fail)
    response = client.post(
        "/accounts/login/",
        {"login": "parent@example.test", "password": "private-form-password"},
    )
    assert response.status_code == 503
    assert b"Temporarily unavailable" in response.content
    assert b"private" not in response.content
    assert "no-store" in response.headers["Cache-Control"]
