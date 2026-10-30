from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from threading import Barrier

import pytest
from django.db import close_old_connections
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from chores.models import Definition, Occurrence
from chores.services import save_one_off
from households.models import BoardAuthority, Child
from households.services import Conflict
from tests.integration.test_pins import fixture, setup, unlock


def prepared():
    a, b, h, c = fixture()
    setup(c, h, a)
    unlock(c, h, a)
    child = Child.objects.create(household=h, name="Aster", pin_hash="synthetic")
    return a, b, h, c, child


def values(assigned, **extra):
    return {
        "title": "Water plants",
        "child": assigned.pk,
        "due_date": "2026-10-25",
        **extra,
    }


@pytest.mark.django_db
def test_create_edit_reassign_delete_revision_and_restore():
    a, _, h, c, child = prepared()
    new = reverse("chore_create", args=[h.pk])
    h.refresh_from_db()
    revision = h.revision
    assert c.post(new, values(child)).status_code == 302
    work = Occurrence.objects.get()
    assert work.definition.title == work.title == "Water plants"
    other = Child.objects.create(household=h, name="Birch", pin_hash="synthetic")
    edit = reverse("chore_edit", args=[h.pk, work.pk])
    assert (
        c.post(edit, values(other, title="Rake leaves", version=1)).status_code == 302
    )
    work.refresh_from_db()
    assert work.child == other and work.definition.child == other and work.version == 2
    assert c.post(edit, values(child, version=1)).status_code == 409
    c.logout()
    c.force_login(a)
    assert b"Rake leaves" in c.get(reverse("household_board", args=[h.pk])).content
    unlock(c, h, a)
    delete = reverse("chore_delete", args=[h.pk, work.pk])
    assert c.post(delete, {"version": 1}).status_code == 409
    assert c.post(delete, {"version": 2}).status_code == 302
    assert not Occurrence.objects.exists() and not Definition.objects.exists()
    h.refresh_from_db()
    assert h.revision == revision + 3


@pytest.mark.django_db
@pytest.mark.parametrize(
    "bad",
    [
        {"title": ""},
        {"child": ""},
        {"child": 999999},
        {"due_date": ""},
        {"due_date": "2026-02-30"},
        {"title": "x" * 201},
    ],
)
def test_invalid_no_partial_work(bad):
    _, _, h, c, child = prepared()
    assert (
        c.post(reverse("chore_create", args=[h.pk]), values(child, **bad)).status_code
        == 400
    )
    assert not Definition.objects.exists() and not Occurrence.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize("state", ["awaiting_approval", "completed"])
def test_protected_states_ui_and_direct_no_history_loss(state):
    _, _, h, c, child = prepared()
    work = save_one_off(
        h, {"title": "Retained", "child": child, "due_date": date(2026, 10, 25)}
    )
    work.state = state
    work.completed_at = timezone.now() if state == "completed" else None
    work.save()
    for route in ("chore_edit", "chore_delete"):
        url = reverse(route, args=[h.pk, work.pk])
        assert c.get(url).status_code == 409
        response = c.post(url, values(child, version=1))
        assert response.status_code == 409 and b"Only to-do" in response.content
    work.refresh_from_db()
    assert work.state == state and work.title == "Retained"
    assert work.definition_id
    board = c.get(reverse("household_board", args=[h.pk])).content
    assert b"Edit chore" not in board and b"Delete chore" not in board


@pytest.mark.django_db
def test_permissions_foreign_child_work_csrf_expiry_and_failure(monkeypatch):
    from allauth.account.models import EmailAddress
    from django.contrib.auth import get_user_model
    from django.db import OperationalError

    from households.services import create_household

    a, _, h, c, child = prepared()
    outsider = get_user_model().objects.create_user(
        username="outside", email="outside@example.test"
    )
    EmailAddress.objects.create(user=outsider, email=outsider.email, verified=True)
    foreign = create_household(outsider, "UTC")
    foreign_child = Child.objects.create(
        household=foreign, name="Other", pin_hash="synthetic"
    )
    work = save_one_off(
        foreign,
        {
            "title": "Private work",
            "child": foreign_child,
            "due_date": date(2026, 10, 25),
        },
    )
    assert (
        c.post(reverse("chore_create", args=[h.pk]), values(foreign_child)).status_code
        == 400
    )
    for route in ("chore_edit", "chore_delete"):
        assert (
            c.post(
                reverse(route, args=[h.pk, work.pk]), values(child, version=1)
            ).status_code
            == 403
        )
    assert c.get(reverse("household_board", args=[foreign.pk])).status_code == 403
    url = reverse("chore_create", args=[h.pk])
    locked = Client()
    locked.force_login(a)
    assert locked.post(url, values(child, pin="0123")).status_code == 403
    outside = Client()
    outside.force_login(outsider)
    assert outside.post(url, values(child)).status_code == 403
    csrf = Client(enforce_csrf_checks=True)
    csrf.force_login(a)
    assert csrf.post(url, values(child)).status_code == 403
    monkeypatch.setattr(
        "chores.views.save_one_off",
        lambda *args: (_ for _ in ()).throw(OperationalError()),
    )
    response = c.post(url, values(child))
    assert response.status_code == 503 and b"Chore saved." not in response.content
    BoardAuthority.objects.update(last_activity=timezone.now() - timedelta(seconds=60))
    assert c.post(url, values(child)).status_code == 403
    assert Occurrence.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_competing_edit_delete_one_explicit_conflict():
    _, _, h, _, child = prepared()
    work = save_one_off(
        h, {"title": "Original", "child": child, "due_date": date(2026, 10, 25)}
    )
    gate = Barrier(2)

    def run(delete):
        close_old_connections()
        try:
            gate.wait(timeout=10)
            try:
                save_one_off(
                    h,
                    {
                        "title": "Changed",
                        "child": child,
                        "due_date": date(2026, 10, 26),
                        "version": 1,
                    },
                    work.pk,
                    delete,
                )
                return "accepted"
            except (
                Conflict,
                __import__(
                    "django.core.exceptions", fromlist=["PermissionDenied"]
                ).PermissionDenied,
            ):
                return "conflict"
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, (False, True)))
    assert sorted(results) == ["accepted", "conflict"]


@pytest.mark.django_db(transaction=True)
def test_real_server_restart_retains_postgresql_work():
    import os
    import socket
    import subprocess
    import sys
    import time
    from urllib.request import Request, urlopen

    from django.conf import settings
    from django.db import connection

    _, _, h, client, child = prepared()
    work = save_one_off(
        h, {"title": "Restart retained", "child": child, "due_date": date(2026, 10, 25)}
    )
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    env = dict(
        os.environ,
        DJANGO_SETTINGS_MODULE="config.settings.local",
        DB_NAME=connection.settings_dict["NAME"],
    )
    url = f"http://127.0.0.1:{port}"
    cookie = f"{settings.SESSION_COOKIE_NAME}={client.cookies[settings.SESSION_COOKIE_NAME].value}"
    for _ in range(2):
        server = subprocess.Popen(
            [
                sys.executable,
                "manage.py",
                "runserver",
                f"127.0.0.1:{port}",
                "--noreload",
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            deadline = time.monotonic() + 10
            while True:
                try:
                    with urlopen(url + "/health/", timeout=1) as response:
                        assert response.status == 200
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise
                    time.sleep(0.1)
            with urlopen(
                Request(
                    url + reverse("household_board", args=[h.pk]),
                    headers={"Cookie": cookie},
                ),
                timeout=3,
            ) as response:
                html = response.read()
                assert (
                    b"Restart retained" in html
                    and f'data-work-id="{work.pk}"'.encode() in html
                )
        finally:
            server.terminate()
            server.wait(timeout=10)
    assert Occurrence.objects.get(pk=work.pk).definition.title == "Restart retained"
