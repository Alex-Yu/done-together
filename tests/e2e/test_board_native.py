"""Installed stable browsers; mixed work is patched internally in the test server only.

Requires project geckodriver on4445. No fixture selection exists in production HTTP.
"""

import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from playwright.sync_api import sync_playwright

from households.models import Child
from tests.integration.test_board import mixed_work
from tests.integration.test_pins import PASS_A, fixture, setup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import verify_household_browsers as native  # noqa: E402


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_BOARD") != "1",
    reason="explicit installed-browser check; requires geckodriver4445",
)
@pytest.mark.django_db(transaction=True)
def test_installed_board_native_zoom_keyboard(live_server, monkeypatch):
    a, _, h, client = fixture()
    setup(client, h, a)
    child = Child.objects.create(
        household=h, name="Aster " + "extraordinarilylongname" * 5, pin_hash="unused"
    )
    Child.objects.create(household=h, name="Birch empty", pin_hash="unused")
    monkeypatch.setattr(
        "board.read_model.load_visible_work", lambda household: mixed_work(child.pk)
    )
    monkeypatch.setattr(native, "BASE_URL", live_server.url)
    with sync_playwright() as playwright:
        for engine in ("chrome", "firefox"):
            for zoom in (1, 2):
                with TemporaryDirectory(
                    dir=ROOT / ".local", prefix="board-native-"
                ) as profile:
                    ui = (
                        native.Chrome(playwright, profile, zoom)
                        if engine == "chrome"
                        else native.Firefox(zoom)
                    )
                    try:
                        native.signin(ui, a.email, PASS_A)
                        ui.apply_zoom()
                        metrics = ui.execute(
                            "({width:innerWidth,height:innerHeight,dpr:devicePixelRatio,overflow:document.documentElement.scrollWidth>innerWidth})"
                        )
                        assert metrics["width"] == 1280 // zoom
                        assert metrics["height"] == 720 // zoom
                        assert not metrics["overflow"]
                        assert (
                            ui.execute(
                                "document.querySelectorAll('.child-column').length"
                            )
                            == 2
                        )
                        assert (
                            ui.execute(
                                "document.querySelectorAll('[data-work-id]').length"
                            )
                            == 4
                        )
                        assert ui.execute(
                            "document.querySelector('[data-work-id=done]').getClientRects().length>0"
                        )
                        assert (
                            ui.execute("document.querySelectorAll('details').length")
                            == 0
                        )
                        assert (
                            ui.execute(
                                "[...document.querySelectorAll('.chore-state')].map(el=>el.textContent).join(' ')"
                            ).find("Overdue")
                            >= 0
                        )
                        assert ui.execute(
                            "document.querySelectorAll('.child-column')[1].textContent.includes('Nothing assigned yet.')"
                        )
                        # Scroll to keyboard target through Tab, not mouse; labeled and focused.
                        native.tab_to(ui, "pin")
                        ui.fill("pin", "2468")
                        native.tab_to(ui, button=True)
                        ui.press("Enter")
                        native.wait_for(
                            ui,
                            "document.getElementById('parent-lock-status').textContent.trim()",
                            "Parent controls unlocked.",
                        )
                        assert ui.execute(
                            "document.querySelector('[data-parent-controls] .child-column')===null"
                        )
                        # Navigate the actual protected settings link and return to persisted child columns.
                        path = ui.execute(
                            "[...document.querySelectorAll('a')].find(el=>el.textContent==='Manage household settings').getAttribute('href')"
                        )
                        ui.goto(path)
                        native.wait_heading(ui, "Household settings")
                        ui.goto(f"/households/{h.pk}/board/")
                        native.wait_heading(ui, "Done Together")
                        ui.apply_zoom()
                        ui.screenshot(ROOT / f".local/board-{engine}-{zoom * 100}.png")
                        print(
                            engine,
                            ui.version,
                            zoom * 100,
                            metrics,
                            "mixed states/keyboard/settings/revisit PASS",
                        )
                    finally:
                        ui.close()
