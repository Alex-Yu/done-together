"""Targeted installed Chrome/Firefox 100/200% one-off journeys."""

import os
import sys
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from playwright.sync_api import sync_playwright

from chores.models import Occurrence
from chores.services import save_one_off
from households.models import Child
from tests.integration.test_pins import PASS_A, fixture, setup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import verify_household_browsers as native  # noqa: E402


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_CHORES") != "1",
    reason="requires installed browsers/geckodriver4445",
)
@pytest.mark.django_db(transaction=True)
def test_native_one_off_keyboard_errors_and_timezone(live_server, monkeypatch):
    # Playwright sync owns an event loop; ORM observations remain synchronous
    # in this isolated test thread, never in production requests.
    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    a, _, h, client = fixture()
    setup(client, h, a)
    child = Child.objects.create(household=h, name="Aster", pin_hash="synthetic")
    protected = save_one_off(
        h, {"title": "Awaiting fixture", "child": child, "due_date": date(2026, 3, 8)}
    )
    protected.state = "awaiting_approval"
    protected.save()
    monkeypatch.setattr(native, "BASE_URL", live_server.url)
    output = ROOT / ".local/verification/005"
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        for engine in ("chrome", "firefox"):
            for zoom in (1, 2):
                with TemporaryDirectory(
                    dir=ROOT / ".local", prefix="chores-native-"
                ) as profile:
                    ui = (
                        native.Chrome(playwright, profile, zoom)
                        if engine == "chrome"
                        else native.Firefox(zoom)
                    )
                    try:
                        native.signin(ui, a.email, PASS_A)
                        ui.fill("pin", "2468")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_for(
                            ui,
                            "document.getElementById('parent-lock-status').textContent.trim()",
                            "Parent controls unlocked.",
                        )
                        ui.goto(f"/households/{h.pk}/chores/new/")
                        native.wait_heading(ui, "Assign one-off chore")
                        ui.apply_zoom()
                        assert ui.execute(
                            "document.querySelector('[name=child]').textContent.includes('Aster')"
                        )
                        assert ui.execute("innerWidth") == 1280 // zoom
                        assert ui.execute("innerHeight") == 720 // zoom
                        native.tab_to(ui, "title")
                        ui.fill("title", f"{engine} {zoom} plants")
                        native.tab_to(ui, "child")
                        # Native select popup key handling depends on OS; select its option
                        # after verifying keyboard focus and label via tab_to.
                        ui.execute(
                            f"document.querySelector('[name=child]').value='{child.pk}'"
                        )
                        native.tab_to(ui, "due_date")
                        # ISO date entry differs in native date widgets; set its calendar value.
                        ui.execute(
                            "document.querySelector('[name=due_date]').value='2026-03-08'"
                        )
                        native.tab_to(ui, button=True)
                        assert ui.execute(
                            "document.querySelector('form').checkValidity()"
                        ), ui.execute(
                            "[...document.querySelectorAll('input,select')].map(e=>[e.name,e.value,e.validationMessage])"
                        )
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        work = Occurrence.objects.filter(
                            title=f"{engine} {zoom} plants"
                        ).get()
                        ui.goto(f"/households/{h.pk}/chores/{work.pk}/edit/")
                        native.wait_heading(ui, "Edit chore")
                        ui.execute("document.querySelector('form').noValidate=true")
                        native.tab_to(ui, "title")
                        ui.fill("title", "")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_for(
                            ui,
                            "document.body.textContent.includes('This field is required.')",
                            True,
                        )
                        assert not ui.execute(
                            "document.documentElement.scrollWidth>innerWidth"
                        )
                        ui.screenshot(output / f"{engine}-{zoom * 100}-error.png")
                        ui.fill("title", f"{engine} {zoom} edited")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        ui.goto(f"/households/{h.pk}/chores/{protected.pk}/delete/")
                        native.wait_heading(ui, "Delete chore")
                        assert ui.execute(
                            "document.querySelector('button[type=submit]')===null"
                        )
                        ui.goto(f"/households/{h.pk}/chores/{work.pk}/delete/")
                        native.wait_heading(ui, "Delete chore")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        assert not Occurrence.objects.filter(pk=work.pk).exists()
                        ui.apply_zoom()
                        assert not ui.execute(
                            "document.documentElement.scrollWidth>innerWidth"
                        )
                        ui.screenshot(output / f"{engine}-{zoom * 100}-board.png")
                        print(
                            engine,
                            ui.version,
                            zoom * 100,
                            "keyboard/focus/labels/create/error/edit/delete/protected state PASS",
                        )
                    finally:
                        ui.close()
        # Same server date snapshot, browser-local calendar at DST boundary.
        work = save_one_off(
            h, {"title": "Timezone work", "child": child, "due_date": date(2026, 3, 8)}
        )
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        try:
            for zone, expected in [
                ("America/Los_Angeles", False),
                ("Europe/Warsaw", True),
            ]:
                context = browser.new_context(timezone_id=zone)
                page = context.new_page()
                page.clock.install(
                    time=__import__("datetime").datetime(
                        2026, 3, 9, 0, 30, tzinfo=__import__("datetime").timezone.utc
                    )
                )
                page.goto(live_server.url + "/accounts/login/")
                page.locator("[name=login]").fill(a.email)
                page.locator("[name=password]").fill(PASS_A)
                page.get_by_role("button", name="Sign in", exact=True).click()
                card = page.locator(f'[data-work-id="{work.pk}"]')
                assert card.get_attribute("data-local-due") == "2026-03-08"
                assert card.locator("[data-overdue]").is_visible() == expected
                context.close()
            print("DST-boundary timezone identity/date/local overdue PASS")
        finally:
            browser.close()
            from django.db import connections

            connections.close_all()
