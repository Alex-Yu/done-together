"""Actual approval-derived progress in installed stable browsers at native zoom."""

import os
import sys
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from django.utils import timezone
from playwright.sync_api import sync_playwright

from tests.integration.test_pins import PASS_A
from tests.integration.test_review import ready
from tests.integration.test_stars import approve

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import verify_household_browsers as native  # noqa: E402


@pytest.mark.skipif(
    os.environ.get("RUN_NATIVE_STARS") != "1",
    reason="installed browsers/geckodriver4445 required",
)
@pytest.mark.django_db(transaction=True)
def test_native_visible_completions_totals_keyboard_zoom(live_server, monkeypatch):
    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    a, _, h, c, child, active = ready()
    now = timezone.now()
    approve(h, c, a, child, "Current earned completion", now)
    approve(h, c, a, child, "Hidden old completion", now - timedelta(days=14))
    monkeypatch.setattr(native, "BASE_URL", live_server.url)
    output = ROOT / ".local/verification/008"
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        for engine in ("chrome", "firefox"):
            for zoom in (1, 2):
                with TemporaryDirectory(
                    dir=ROOT / ".local", prefix="stars-native-"
                ) as profile:
                    ui = (
                        native.Chrome(playwright, profile, zoom)
                        if engine == "chrome"
                        else native.Firefox(zoom)
                    )
                    try:
                        native.signin(ui, a.email, PASS_A)
                        ui.apply_zoom()
                        assert ui.execute("innerWidth") == 1280 // zoom
                        assert ui.execute("innerHeight") == 720 // zoom
                        text = ui.execute("document.body.textContent")
                        assert (
                            "This week: 1 star" in text and "All time: 2 stars" in text
                        )
                        assert (
                            "Current earned completion" in text
                            and "Hidden old completion" not in text
                        )
                        assert active.title in text and "Completed" in text
                        assert not ui.execute("!!document.querySelector('details')")
                        assert not ui.execute(
                            "document.documentElement.scrollWidth>innerWidth"
                        )
                        native.tab_to(ui, "pin")
                        assert ui.execute("document.activeElement.labels.length") > 0
                        assert (
                            ui.execute(
                                "getComputedStyle(document.activeElement).outlineStyle"
                            )
                            != "none"
                        )
                        ui.execute(
                            "document.querySelector('[data-star-totals]').scrollIntoView()"
                        )
                        ui.screenshot(output / f"{engine}-{zoom * 100}.png")
                        ui.goto(f"/households/{h.pk}/board/")
                        native.wait_heading(ui, "Done Together")
                        assert "All time: 2 stars" in ui.execute(
                            "document.body.textContent"
                        )
                        print(
                            engine,
                            ui.version,
                            zoom * 100,
                            "actual stars/completions/reload/keyboard/zoom PASS",
                        )
                    finally:
                        ui.close()
        from django.db import connections

        connections.close_all()
    connections.close_all()
