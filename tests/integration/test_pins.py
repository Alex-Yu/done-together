from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from django.test import Client, override_settings
from django.urls import reverse
from django.utils import timezone

from accounts.limits import private_key
from accounts.models import AuthenticationLimit
from households.models import BoardAuthority, Child, Membership, ParentCredential
from households.pins import verify_child_pin
from households.services import create_household

PASS_A = "Synthetic-Parent-A-7392!"
PASS_B = "Synthetic-Parent-B-8426!"


def fixture():
    a = get_user_model().objects.create_user(
        username="first", email="first@example.test", password=PASS_A
    )
    b = get_user_model().objects.create_user(
        username="second", email="second@example.test", password=PASS_B
    )
    for u in (a, b):
        EmailAddress.objects.create(user=u, email=u.email, verified=True, primary=True)
    household = create_household(a, "Europe/Warsaw")
    Membership.objects.create(user=b, household=household, slot=2)
    client = Client()
    client.force_login(a)
    return a, b, household, client


def setup(client, household, parent, password=PASS_A, pin="2468"):
    return client.post(
        reverse("parent_pin", args=[household.pk]),
        {"parent": parent.pk, "password": password, "pin": pin},
    )


def unlock(client, household, parent, pin="2468"):
    return client.post(
        reverse("parent_unlock", args=[household.pk]), {"parent": parent.pk, "pin": pin}
    )


@pytest.mark.django_db
def test_selected_own_password_setup_either_parent_unlock_and_reset_invalidation():
    a, b, h, c = fixture()
    assert setup(c, h, b, password=PASS_A).status_code == 400
    assert not ParentCredential.objects.filter(user=b).exists()
    assert setup(c, h, b, password=PASS_B, pin="0007").status_code == 302
    assert unlock(c, h, b, "0007").status_code == 302
    assert BoardAuthority.objects.get().parent == b
    assert c.get(reverse("household_settings", args=[h.pk])).status_code == 200
    separate = Client()
    separate.force_login(a)
    assert (
        separate.post(
            reverse("child_create", args=[h.pk]), {"name": "Aster", "pin": "0123"}
        ).status_code
        == 403
    )
    assert unlock(separate, h, b, "0007").status_code == 302
    assert setup(c, h, b, password=PASS_B, pin="0123").status_code == 302
    for client in (c, separate):
        assert (
            client.post(
                reverse("child_create", args=[h.pk]), {"name": "Aster", "pin": "0007"}
            ).status_code
            == 403
        )
        assert unlock(client, h, b, "0007").status_code == 400
    assert unlock(c, h, b, "0123").status_code == 302
    credential = ParentCredential.objects.get(user=b)
    assert credential.pin_hash.startswith("argon2$") and credential.pin_hash != "0123"


@pytest.mark.django_db
def test_child_add_edit_reset_and_pin_checks_cannot_grant_parent_authority():
    a, _, h, c = fixture()
    setup(c, h, a)
    unlock(c, h, a)
    assert (
        c.post(
            reverse("child_create", args=[h.pk]), {"name": "Aster", "pin": "0007"}
        ).status_code
        == 302
    )
    child = Child.objects.get()
    assert verify_child_pin(a, h.pk, child.pk, "0007")
    assert (
        c.post(
            reverse("child_edit", args=[h.pk, child.pk]),
            {
                "name": "Birch",
                "revision": c.get(reverse("child_edit", args=[h.pk, child.pk]))
                .context["form"]
                .initial["revision"],
            },
        ).status_code
        == 302
    )
    assert (
        c.post(reverse("child_pin", args=[h.pk, child.pk]), {"pin": "0123"}).status_code
        == 302
    )
    child.refresh_from_db()
    assert child.name == "Birch" and child.pin_hash.startswith("argon2$")
    assert not verify_child_pin(a, h.pk, child.pk, "0007")
    assert verify_child_pin(a, h.pk, child.pk, "0123")
    assert (
        b'value="0123"'
        not in c.get(reverse("child_pin", args=[h.pk, child.pk])).content
    )
    assert (
        child.pin_hash.encode()
        not in c.get(reverse("household_settings", args=[h.pk])).content
    )
    separate = Client()
    separate.force_login(a)
    with override_settings(ROOT_URLCONF="tests.integration.pin_boundary_urls"):
        assert separate.post(
            reverse("fixture_child_check", args=[h.pk, child.pk]), {"pin": "0123"}
        ).json() == {"verified": True}
    assert (
        separate.post(
            reverse("child_create", args=[h.pk]), {"name": "Other", "pin": "1234"}
        ).status_code
        == 403
    )
    assert unlock(separate, h, a, "0123").status_code == 400


@pytest.mark.django_db
@pytest.mark.parametrize(
    "pin", ["", "123", "12345", "１２３４", "١٢٣٤", "0007\n", " 0007"]
)
def test_non_ascii_or_non_four_digit_pin_leaves_no_partial_child(pin):
    a, _, h, c = fixture()
    setup(c, h, a)
    unlock(c, h, a)
    assert (
        c.post(
            reverse("child_create", args=[h.pk]), {"name": "Aster", "pin": pin}
        ).status_code
        == 400
    )
    assert not Child.objects.exists()


@pytest.mark.django_db
def test_timeout_boundary_views_child_checks_and_failed_parent_actions_do_not_extend(
    monkeypatch,
):
    a, _, h, c = fixture()
    setup(c, h, a)
    now = timezone.now()
    monkeypatch.setattr("households.pins.timezone.now", lambda: now)
    unlock(c, h, a)
    start = BoardAuthority.objects.get().last_activity
    now += timedelta(seconds=30)
    assert c.post(reverse("parent_activity", args=[h.pk])).status_code == 200
    last = BoardAuthority.objects.get().last_activity
    assert last == now
    now += timedelta(seconds=20)
    assert (
        c.post(
            reverse("child_create", args=[h.pk]), {"name": "", "pin": "0007"}
        ).status_code
        == 400
    )
    c.get(reverse("household_board", args=[h.pk]))
    assert BoardAuthority.objects.get().last_activity == last and last != start
    now += timedelta(seconds=39)
    assert c.get(reverse("household_settings", args=[h.pk])).status_code == 200
    assert BoardAuthority.objects.get().last_activity == last
    now += timedelta(seconds=1)
    assert c.get(reverse("household_settings", args=[h.pk])).status_code == 302
    assert (
        c.post(
            reverse("child_create", args=[h.pk]), {"name": "Aster", "pin": "0007"}
        ).status_code
        == 403
    )
    board = c.get(reverse("household_board", args=[h.pk]))
    assert board.status_code == 200 and b"Parent controls locked" in board.content
    assert BoardAuthority.objects.get().last_activity == last


@pytest.mark.django_db
def test_pin_identity_five_failures_shared_restricted_deadline_and_exact_retry(
    monkeypatch,
):
    a, _, h, c = fixture()
    setup(c, h, a)
    now = timezone.now()
    monkeypatch.setattr("households.pins.timezone.now", lambda: now)
    for _ in range(5):
        other = Client()
        other.force_login(a)
        assert unlock(other, h, a, "9999").status_code == 400
    limit = AuthenticationLimit.objects.get(key=private_key("parent-pin", str(a.pk)))
    deadline = limit.blocked_until
    assert deadline == now + timedelta(minutes=5)
    assert unlock(c, h, a).status_code == 400
    now += timedelta(seconds=299)
    unlock(c, h, a, "9999")
    limit.refresh_from_db()
    assert limit.blocked_until == deadline
    now += timedelta(seconds=1)
    assert unlock(c, h, a).status_code == 302
    limit.refresh_from_db()
    assert limit.failures == 0 and limit.blocked_until is None


@pytest.mark.django_db
def test_parent_pin_password_checks_share_account_password_limit(monkeypatch):
    a, _, h, c = fixture()
    now = timezone.now()
    monkeypatch.setattr("households.pins.timezone.now", lambda: now)
    for _ in range(5):
        assert setup(c, h, a, password="incorrect").status_code == 400
    assert setup(c, h, a).status_code == 400
    assert not ParentCredential.objects.exists()
    login = Client().post("/accounts/login/", {"login": a.email, "password": PASS_A})
    assert login.status_code == 200
    now += timedelta(minutes=5)
    assert setup(c, h, a, pin="0007").status_code == 302


@pytest.mark.django_db
def test_foreign_parent_child_household_and_locked_settings_are_denied():
    a, _, h, c = fixture()
    assert c.get(reverse("household_settings", args=[h.pk])).status_code == 302
    assert (
        c.post(
            reverse("household_settings", args=[h.pk]), {"email": "new@example.test"}
        ).status_code
        == 403
    )
    outsider = get_user_model().objects.create_user(
        username="outsider", email="outside@example.test", password=PASS_A
    )
    EmailAddress.objects.create(
        user=outsider, email=outsider.email, verified=True, primary=True
    )
    foreign = create_household(outsider, "UTC")
    assert setup(c, h, outsider).status_code == 400
    setup(c, h, a)
    unlock(c, h, a)
    child = Child.objects.create(household=foreign, name="Private child", pin_hash="")
    assert (
        c.post(reverse("child_pin", args=[h.pk, child.pk]), {"pin": "0007"}).status_code
        == 403
    )
    assert c.get(reverse("household_board", args=[foreign.pk])).status_code == 403
    assert not c.get(reverse("parent_pin", args=[h.pk])).content.count(
        outsider.email.encode()
    )


@pytest.mark.django_db(transaction=True)
def test_concurrent_pin_failures_are_not_lost():
    a, _, h, c = fixture()
    setup(c, h, a)
    unlock(c, h, a)
    c.post(reverse("child_create", args=[h.pk]), {"name": "Aster", "pin": "0007"})
    child = Child.objects.get()
    barrier = Barrier(5)

    def fail(_):
        close_old_connections()
        try:
            barrier.wait(timeout=10)
            return bool(verify_child_pin(a, h.pk, child.pk, "9999"))
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=5) as pool:
        assert list(pool.map(fail, range(5))) == [False] * 5
    limit = AuthenticationLimit.objects.get(key=private_key("child-pin", str(child.pk)))
    assert limit.failures == 5 and limit.blocked_until is not None
    assert not verify_child_pin(a, h.pk, child.pk, "0007")


@pytest.mark.django_db
def test_pin_mutations_require_csrf_and_database_failure_does_not_echo_input(
    monkeypatch, settings
):
    from django.db import OperationalError

    a, _, h, c = fixture()
    csrf = Client(enforce_csrf_checks=True)
    csrf.force_login(a)
    for route in ("parent_pin", "parent_unlock", "parent_activity", "child_create"):
        assert (
            csrf.post(
                reverse(route, args=[h.pk]),
                {"parent": a.pk, "pin": "0007", "password": PASS_A},
            ).status_code
            == 403
        )
    settings.DEBUG = True

    def fail(*args, **kwargs):
        raise OperationalError("synthetic-private-pin-fault")

    monkeypatch.setattr("households.pin_views.set_parent_pin", fail)
    c.raise_request_exception = False
    response = setup(c, h, a, pin="0007")
    assert (
        response.status_code == 503
        and b"synthetic-private" not in response.content
        and PASS_A.encode() not in response.content
        and b'value="0007"' not in response.content
    )


@pytest.mark.django_db
def test_selected_inactive_parent_revokes_grant_opened_by_other_parent():
    a, b, h, c = fixture()
    setup(c, h, b, password=PASS_B, pin="0007")
    unlock(c, h, b, "0007")
    assert c.get(reverse("household_settings", args=[h.pk])).status_code == 200
    b.is_active = False
    b.save(update_fields=["is_active"])
    assert c.get(reverse("household_settings", args=[h.pk])).status_code == 302
    assert (
        c.post(
            reverse("child_create", args=[h.pk]), {"name": "Aster", "pin": "0123"}
        ).status_code
        == 403
    )
    assert (
        b"Parent controls locked"
        in c.get(reverse("household_board", args=[h.pk])).content
    )


@pytest.mark.django_db(transaction=True)
def test_reset_racing_verified_old_pin_cannot_grant_new_credential_version(monkeypatch):
    from threading import Event

    import households.pins as pins

    a, b, h, c = fixture()
    setup(c, h, b, password=PASS_B, pin="0007")
    verified = Event()
    release = Event()
    reset_started = Event()
    original = pins.verify_parent_pin

    def pause_after_verification(*args, **kwargs):
        valid = original(*args, **kwargs)
        verified.set()
        assert release.wait(timeout=10)
        return valid

    monkeypatch.setattr(pins, "verify_parent_pin", pause_after_verification)

    def granting():
        close_old_connections()
        try:
            client = Client()
            client.force_login(a)
            return unlock(client, h, b, "0007").status_code
        finally:
            close_old_connections()

    def resetting():
        close_old_connections()
        try:
            client = Client()
            client.force_login(a)
            reset_started.set()
            return setup(client, h, b, password=PASS_B, pin="0123").status_code
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(granting)
        assert verified.wait(timeout=10)
        second = pool.submit(resetting)
        assert reset_started.wait(timeout=10)
        assert not second.done()
        release.set()
        assert first.result(timeout=10) == 302 and second.result(timeout=10) == 302
    authority = BoardAuthority.objects.get()
    credential = ParentCredential.objects.get(user=b)
    assert authority.credential_version < credential.version
    assert not pins.authority_valid(authority)


@pytest.mark.django_db
@override_settings(ROOT_URLCONF="tests.integration.pin_boundary_urls")
def test_child_activity_never_extends_parent_deadline(monkeypatch):
    a, _, h, c = fixture()
    setup(c, h, a)
    unlock(c, h, a)
    c.post(reverse("child_create", args=[h.pk]), {"name": "Aster", "pin": "0007"})
    child = Child.objects.get()
    now = timezone.now()
    monkeypatch.setattr("households.pins.timezone.now", lambda: now)
    unlock(c, h, a)
    deadline_start = BoardAuthority.objects.get().last_activity
    now += timedelta(seconds=59)
    response = c.post(
        reverse("fixture_child_check", args=[h.pk, child.pk]), {"pin": "0007"}
    )
    assert response.json() == {"verified": True}
    assert BoardAuthority.objects.get().last_activity == deadline_start
    now += timedelta(seconds=1)
    assert c.post(reverse("parent_activity", args=[h.pk])).status_code == 403
    assert b"Aster" in c.get(reverse("household_board", args=[h.pk])).content


@pytest.mark.django_db
@override_settings(ROOT_URLCONF="tests.integration.pin_boundary_urls")
def test_child_pin_shared_restriction_expires_without_extension(monkeypatch):
    a, _, h, c = fixture()
    setup(c, h, a)
    unlock(c, h, a)
    c.post(reverse("child_create", args=[h.pk]), {"name": "Aster", "pin": "0007"})
    child = Child.objects.get()
    now = timezone.now()
    monkeypatch.setattr("households.pins.timezone.now", lambda: now)
    for _ in range(5):
        separate = Client()
        separate.force_login(a)
        assert separate.post(
            reverse("fixture_child_check", args=[h.pk, child.pk]), {"pin": "9999"}
        ).json() == {"verified": False}
    limit = AuthenticationLimit.objects.get(key=private_key("child-pin", str(child.pk)))
    deadline = limit.blocked_until
    assert deadline == now + timedelta(minutes=5)
    now += timedelta(seconds=299)
    assert c.post(
        reverse("fixture_child_check", args=[h.pk, child.pk]), {"pin": "0007"}
    ).json() == {"verified": False}
    limit.refresh_from_db()
    assert limit.blocked_until == deadline
    assert unlock(c, h, a).status_code == 302
    now += timedelta(seconds=1)
    assert c.post(
        reverse("fixture_child_check", args=[h.pk, child.pk]), {"pin": "0007"}
    ).json() == {"verified": True}
    limit.refresh_from_db()
    assert limit.failures == 0 and limit.blocked_until is None


@pytest.mark.django_db
def test_exact_password_whitespace_and_external_pepper_are_required():
    from django.contrib.auth.hashers import check_password

    from households.pins import verify_parent_pin

    a, _, h, c = fixture()
    password = " " + PASS_A + " "
    a.set_password(password)
    a.save(update_fields=["password"])
    c.force_login(a)
    assert setup(c, h, a, password=password, pin="0007").status_code == 302
    credential = ParentCredential.objects.get(user=a)
    assert not check_password("0007", credential.pin_hash)
    assert verify_parent_pin(a, h.pk, a.pk, "0007")
    with override_settings(PIN_HASH_PEPPER="synthetic-alternative-pepper"):
        assert not verify_parent_pin(a, h.pk, a.pk, "0007")
