"""Fresh integrated J01-J05 keyboard journey in installed stable browsers.

Email capture here is isolated in-memory; the separate SMTP gate uses Mailpit.
No application fixtures or DOM value/focus writes substitute for user actions.
"""

import json
import os
import secrets
import sys
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from playwright.sync_api import sync_playwright

from tests.e2e.test_accounts import captured_path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import verify_household_browsers as native  # noqa: E402
from verify_release_keyboard import Keyboard  # noqa: E402


def signin(k, email, password):
    k.heading("Sign in")
    k.text("login", email)
    k.text("password", password)
    k.button("Sign in")
    k.heading("Done Together")


def signup(k, email, password, mailoutbox):
    k.text("email", email)
    k.text("password1", password)
    k.text("password2", password)
    k.button("Create account")
    k.heading("Check your email")
    k.ui.goto(captured_path(mailoutbox, "confirm-email/"))
    k.heading("Verify your email")
    k.button("Verify email")


def unlock(k):
    k.text("pin", "2468")
    k.button("Unlock parent controls")
    native.wait_for(
        k.ui,
        "document.getElementById('parent-lock-status').textContent.trim()",
        "Parent controls unlocked.",
    )


def pin_setup(k, password):
    k.link("Set or reset your own parent PIN")
    k.heading("Set or reset your parent PIN")
    k.text("password", password)
    k.text("pin", "2468")
    k.button("Save parent PIN")
    k.heading("Done Together")
    unlock(k)


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_RELEASE") != "1",
    reason="installed stable browsers/driver required",
)
@pytest.mark.parametrize("engine", ["chrome", "firefox"])
@pytest.mark.parametrize("zoom", [1, 2])
@pytest.mark.django_db(transaction=True)
def test_keyboard_integrated_household_work_review_recovery(
    live_server, monkeypatch, mailoutbox, engine, zoom
):
    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    monkeypatch.setattr(native, "BASE_URL", live_server.url)
    output = ROOT / ".local/verification/010"
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        with TemporaryDirectory(
            dir=ROOT / ".local", prefix="release-native-"
        ) as profile:
            ui = (
                native.Chrome(playwright, profile, zoom)
                if engine == "chrome"
                else native.Firefox(zoom)
            )
            k = Keyboard(ui)
            email = f"release-{secrets.token_hex(6)}@example.test"
            recipient = f"recipient-{secrets.token_hex(6)}@example.test"
            password = "Synthetic-Release-4829!"
            try:
                ui.goto("/accounts/signup/")
                k.heading("Create account")
                signup(k, email, password, mailoutbox)
                signin(k, email, password)
                k.heading("Done Together")
                # Verified account entry redirects to household bootstrap.
                k.link("Household settings")
                k.heading("Create your household")
                k.field("timezone")
                k.button("Create household")
                k.heading("Done Together")
                assert ui.execute(
                    "document.body.textContent.includes('Let’s set up your board')"
                )
                pin_setup(k, password)
                k.link("Manage household settings")
                k.heading("Household settings")
                k.link("Add child")
                k.heading("Add child")
                k.text("name", "Aster keyboard")
                k.text("pin", "0007")
                k.button("Save child")
                k.heading("Household settings")
                k.text("email", recipient)
                k.button("Send invitation")
                k.heading("Household settings")
                invite = captured_path(mailoutbox, "households/invitations/")
                k.link("Sign out")
                k.button("Sign out")
                k.heading("Sign in")
                k.link("Create account")
                k.heading("Create account")
                signup(k, recipient, password, mailoutbox)
                signin(k, recipient, password)
                ui.goto(invite)
                k.heading("Join the household")
                k.button("Join household")
                k.heading("Done Together")
                pin_setup(k, password)
                # J02/J03: real one-off creation and return/resubmission.
                k.link("Assign one-off chore")
                k.heading("Assign one-off chore")
                k.text("title", "Water keyboard plants")
                k.select(
                    "child",
                    ui.execute(
                        "document.querySelector('[name=child]').options[1].value"
                    ),
                )
                k.date("due_date", date.today().isoformat())
                k.button("Save chore")
                k.heading("Done Together")
                k.link("Submit chore")
                k.heading("Submit chore")
                k.text("pin", "0007")
                k.button("Submit for approval")
                k.heading("Done Together")
                k.link("Review chore")
                k.heading("Review chore")
                k.select("action", "return")
                k.button("Save review")
                k.heading("Review chore")
                assert ui.execute(
                    "document.body.textContent.includes('Explain what needs doing')"
                )
                k.text("note", "Please water the small pot too.")
                k.button("Save review")
                k.heading("Done Together")
                k.link("Submit chore")
                k.heading("Submit chore")
                k.text("pin", "0007")
                k.button("Submit for approval")
                k.heading("Done Together")
                k.link("Review chore")
                k.heading("Review chore")
                k.select("action", "approve")
                k.button("Save review")
                k.heading("Done Together")
                assert ui.execute(
                    "document.body.textContent.includes('All time: 1 star')"
                )
                # J04: both schedule types through actual keyboard controls.
                for schedule in ("daily", "weekdays"):
                    k.link("Assign recurring chore")
                    k.heading("Assign recurring chore")
                    k.text("title", schedule + " keyboard")
                    k.select(
                        "child",
                        ui.execute(
                            "document.querySelector('[name=child]').options[1].value"
                        ),
                    )
                    k.select("schedule", schedule)
                    if schedule == "weekdays":
                        k.field("weekdays")
                        for index in range(7):
                            k.key("Space")
                            if index < 6:
                                k.key("Tab")
                    k.button("Save schedule")
                    k.heading("Done Together")
                k.link("Edit recurring chore")
                k.heading("Edit recurring chore")
                k.text("title", "Future keyboard title")
                k.select("schedule", "weekdays")
                k.field("weekdays")
                k.key("Space")
                k.button("Save schedule")
                k.heading("Done Together")
                assert ui.execute(
                    "document.body.textContent.includes('daily keyboard')"
                )
                k.link("Delete recurring chore")
                k.heading("Delete recurring chore")
                k.button("Delete recurring chore")
                k.heading("Done Together")
                # J05: protected reset, old PIN rejection, signout/recovery.
                k.link("Manage household settings")
                k.heading("Household settings")
                k.link("Reset child PIN")
                k.heading("Reset child PIN")
                k.text("pin", "0123")
                k.button("Save child")
                k.heading("Household settings")
                k.link("Return to board")
                k.heading("Done Together")
                k.link("Submit chore")
                k.heading("Submit chore")
                k.text("pin", "0007")
                k.button("Submit for approval")
                k.heading("Submit chore")
                assert ui.execute(
                    "document.body.textContent.includes('Unable to submit.')"
                )
                k.text("pin", "0123")
                k.button("Submit for approval")
                k.heading("Done Together")
                ui.screenshot(output / f"keyboard-{engine}-{zoom * 100}-board.png")
                k.link("Sign out")
                k.button("Sign out")
                k.heading("Sign in")
                k.link("Forgot your password?")
                k.heading("Reset your password")
                k.text("email", recipient)
                k.button("Send recovery email")
                k.heading("Check your email")
                ui.goto(captured_path(mailoutbox, "password/reset/key/"))
                k.heading("Choose a new password")
                replacement = "Replacement-Release-4932!"
                k.text("password1", replacement)
                k.text("password2", replacement)
                k.button("Save new password")
                k.heading("Password updated")
                k.link("Sign in")
                signin(k, recipient, replacement)
                k.heading("Done Together")
                assert ui.execute(
                    "document.body.textContent.includes('All time: 1 star')"
                )
                ui.screenshot(output / f"keyboard-{engine}-{zoom * 100}-recovered.png")
                print(
                    engine,
                    ui.version,
                    zoom * 100,
                    "fresh keyboard J01-J05 registration/invite/native date/select/return/approval/schedules/reset/recovery/revisit PASS",
                    flush=True,
                )
            except Exception:
                state = ui.execute(
                    "({heading:document.querySelector('h1')?.textContent,connected:document.documentElement.dataset.connected,controls:[...document.querySelectorAll('input,select,textarea,button,a')].map(e=>({tag:e.tagName,name:e.name,disabled:e.disabled,aria:e.getAttribute('aria-disabled'),locked:e.dataset.parentLocked,text:e.tagName==='A'||e.tagName==='BUTTON'?e.textContent.trim():''}))})"
                )
                (output / f"keyboard-{engine}-{zoom * 100}-failure.json").write_text(
                    json.dumps(state, indent=2)
                )
                ui.screenshot(output / f"keyboard-{engine}-{zoom * 100}-failure.png")
                raise
            finally:
                ui.close()
        from django.db import connections

        connections.close_all()
