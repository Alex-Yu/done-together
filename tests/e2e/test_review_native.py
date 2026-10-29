"""Installed stable-browser submission/review delta, native100/200%."""

import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from playwright.sync_api import sync_playwright

from chores.models import Approval
from chores.services import save_one_off
from tests.integration.test_pins import PASS_A
from tests.integration.test_review import ready

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import verify_household_browsers as native  # noqa: E402


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_REVIEW") != "1",
    reason="installed browsers and geckodriver4445 required",
)
@pytest.mark.django_db(transaction=True)
def test_native_submission_return_resubmit_approval(live_server, monkeypatch):
    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    parent, _, household, _, child, original = ready()
    monkeypatch.setattr(native, "BASE_URL", live_server.url)
    output = ROOT / ".local/verification/007"
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        for engine in ("chrome", "firefox"):
            for zoom in (1, 2):
                work = save_one_off(
                    household,
                    {
                        "title": f"{engine} {zoom} review",
                        "child": child,
                        "due_date": original.due_date,
                    },
                )
                with TemporaryDirectory(
                    dir=ROOT / ".local", prefix="review-native-"
                ) as profile:
                    ui = (
                        native.Chrome(playwright, profile, zoom)
                        if engine == "chrome"
                        else native.Firefox(zoom)
                    )
                    try:
                        native.signin(ui, parent.email, PASS_A)
                        ui.fill("pin", "2468")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_for(
                            ui,
                            "document.getElementById('parent-lock-status').textContent.trim()",
                            "Parent controls unlocked.",
                        )
                        path = f"/households/{household.pk}/chores/{work.pk}"
                        ui.goto(path + "/submit/")
                        native.wait_heading(ui, "Submit chore")
                        ui.apply_zoom()
                        assert ui.execute("innerWidth") == 1280 // zoom
                        assert ui.execute("innerHeight") == 720 // zoom
                        native.tab_to(ui, "pin")
                        ui.fill("pin", "0123")
                        native.tab_to(ui, "browser_timezone")
                        assert ui.execute(
                            "!!document.querySelector('[name=browser_timezone]').value"
                        )
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_for(
                            ui,
                            "document.body.textContent.includes('Unable to submit.')",
                            True,
                        )
                        assert (
                            ui.execute("document.querySelector('[name=pin]').value")
                            == ""
                        )
                        ui.screenshot(output / f"{engine}-{zoom * 100}-error.png")
                        native.tab_to(ui, "pin")
                        ui.fill("pin", "0007")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        ui.goto(path + "/review/")
                        native.wait_heading(ui, "Review chore")
                        native.tab_to(ui, "action")
                        # Native select popup key handling varies by desktop OS.
                        # Verify keyboard focus/label, then assign its selected option.
                        ui.execute(
                            "document.querySelector('[name=action]').value='return'"
                        )
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_for(
                            ui,
                            "document.body.textContent.includes('Explain what needs doing')",
                            True,
                        )
                        native.tab_to(ui, "note")
                        ui.fill("note", "Please water the small pot too.")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        assert ui.execute(
                            "document.body.textContent.includes('Please water the small pot too.')"
                        )
                        assert not ui.execute(
                            "document.documentElement.scrollWidth>innerWidth"
                        )
                        ui.execute(
                            f"document.querySelector('[data-work-id=\"{work.pk}\"]').scrollIntoView()"
                        )
                        ui.screenshot(output / f"{engine}-{zoom * 100}-returned.png")
                        ui.goto(path + "/submit/")
                        native.wait_heading(ui, "Submit chore")
                        native.tab_to(ui, "pin")
                        ui.fill("pin", "0007")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        ui.goto(path + "/review/")
                        native.wait_heading(ui, "Review chore")
                        native.tab_to(ui, "action")
                        ui.execute(
                            "document.querySelector('[name=action]').value='approve'"
                        )
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        assert ui.execute(
                            "document.body.textContent.includes('Chore approved. One star earned.')"
                        )
                        assert Approval.objects.filter(occurrence=work).count() == 1
                        print(
                            engine,
                            ui.version,
                            zoom * 100,
                            "keyboard/PIN error/return note/resubmit/approve PASS",
                        )
                    finally:
                        ui.close()
        # ORM queries made while Playwright's event loop is active use its
        # connection context. Close that context before leaving Playwright.
        from django.db import connections

        connections.close_all()
    connections.close_all()


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_REVIEW") != "1", reason="installed Chrome required"
)
@pytest.mark.django_db(transaction=True)
def test_browser_timezone_submission_classification_survives_viewer_midnight(
    live_server, monkeypatch
):
    from datetime import date, datetime, timedelta, timezone

    from chores.review import review_work

    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    parent, _, household, _, child, _ = ready()
    instant = datetime(2026, 10, 28, 1, tzinfo=timezone.utc)
    monkeypatch.setattr("django.utils.timezone.now", lambda: instant)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        try:
            for zone, late in [("America/Los_Angeles", False), ("Asia/Tokyo", True)]:
                work = save_one_off(
                    household,
                    {"title": zone, "child": child, "due_date": date(2026, 10, 27)},
                )
                context = browser.new_context(timezone_id=zone)
                page = context.new_page()
                page.clock.install(time=instant)
                page.goto(live_server.url + "/accounts/login/")
                page.locator("[name=login]").fill(parent.email)
                page.locator("[name=password]").fill(PASS_A)
                page.get_by_role("button", name="Sign in", exact=True).click()
                page.goto(
                    f"{live_server.url}/households/{household.pk}/chores/{work.pk}/submit/"
                )
                assert page.locator("[name=browser_timezone]").input_value() == zone
                page.locator("[name=pin]").fill("0007")
                page.get_by_role(
                    "button", name="Submit for approval", exact=True
                ).click()
                card = page.locator(f'[data-work-id="{work.pk}"]')
                assert card.locator("[data-overdue]").is_visible() == late
                page.clock.fast_forward(2 * 24 * 3600 * 1000)
                assert card.locator("[data-overdue]").is_visible() == late
                work.refresh_from_db()
                review_work(
                    household,
                    work.pk,
                    work.version,
                    parent,
                    "return",
                    "Try again",
                    now=instant + timedelta(days=2),
                )
                page.reload()
                assert card.locator("[data-overdue]").is_visible()
                context.close()
            print(
                "Server-receipt LA/Tokyo classification/later-midnight preservation/late return PASS"
            )
        finally:
            browser.close()
            from django.db import connections

            connections.close_all()
