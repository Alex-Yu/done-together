"""Targeted installed stable-browser recurrence forms at native100/200%."""

import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from playwright.sync_api import sync_playwright

from chores.models import Definition, Occurrence
from households.models import Child
from tests.integration.test_pins import PASS_A, fixture, setup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import verify_household_browsers as native  # noqa: E402


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_RECURRENCE") != "1",
    reason="installed browsers and geckodriver4445 required",
)
@pytest.mark.django_db(transaction=True)
def test_native_schedule_keyboard_edit_delete(live_server, monkeypatch):
    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    parent, _, household, client = fixture()
    setup(client, household, parent)
    child = Child.objects.create(
        household=household, name="Aster", pin_hash="synthetic"
    )
    monkeypatch.setattr(native, "BASE_URL", live_server.url)
    output = ROOT / ".local/verification/006"
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        for engine in ("chrome", "firefox"):
            for zoom in (1, 2):
                with TemporaryDirectory(
                    dir=ROOT / ".local", prefix="recurrence-native-"
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
                        ui.goto(f"/households/{household.pk}/recurring/new/")
                        native.wait_heading(ui, "Assign recurring chore")
                        ui.apply_zoom()
                        assert ui.execute("innerWidth") == 1280 // zoom
                        assert ui.execute("innerHeight") == 720 // zoom
                        title = f"{engine} {zoom} recurring"
                        native.tab_to(ui, "title")
                        ui.fill("title", title)
                        native.tab_to(ui, "child")
                        ui.execute(
                            f"document.querySelector('[name=child]').value='{child.pk}'"
                        )
                        native.tab_to(ui, "schedule")
                        ui.execute(
                            "document.querySelector('[name=schedule]').value='weekdays'"
                        )
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_for(
                            ui,
                            "document.body.textContent.includes('Choose at least one weekday.')",
                            True,
                        )
                        assert not ui.execute(
                            "document.documentElement.scrollWidth>innerWidth"
                        )
                        ui.screenshot(output / f"{engine}-{zoom * 100}-error.png")
                        # All weekdays ensure due work exists regardless of verification date.
                        for index in range(7):
                            native.tab_to(ui, "weekdays") if index == 0 else ui.press(
                                "Tab"
                            )
                            ui.press("Space")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        definition = Definition.objects.get(title=title)
                        assert definition.weekdays == list(range(7))
                        work = Occurrence.objects.get(definition=definition)
                        ui.goto(
                            f"/households/{household.pk}/recurring/{definition.pk}/edit/"
                        )
                        native.wait_heading(ui, "Edit recurring chore")
                        native.tab_to(ui, "title")
                        ui.fill("title", title + " edited")
                        native.tab_to(ui, "schedule")
                        ui.execute(
                            "document.querySelector('[name=schedule]').value='daily'"
                        )
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        definition.refresh_from_db()
                        work.refresh_from_db()
                        assert (
                            definition.title == title + " edited"
                            and definition.schedule == "daily"
                        )
                        assert work.title == title
                        ui.goto(
                            f"/households/{household.pk}/recurring/{definition.pk}/delete/"
                        )
                        native.wait_heading(ui, "Delete recurring chore")
                        ui.apply_zoom()
                        assert ui.execute(
                            "document.body.textContent.includes('Completed history and earned stars are retained.')"
                        )
                        assert not ui.execute(
                            "document.documentElement.scrollWidth>innerWidth"
                        )
                        ui.screenshot(output / f"{engine}-{zoom * 100}-delete.png")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_heading(ui, "Done Together")
                        assert not Definition.objects.filter(pk=definition.pk).exists()
                        assert not Occurrence.objects.filter(pk=work.pk).exists()
                        print(
                            engine,
                            ui.version,
                            zoom * 100,
                            "schedule/weekday keyboard/validation/future edit/delete PASS",
                        )
                    finally:
                        ui.close()
        from django.db import connections

        connections.close_all()
