"""Supplement bundled-browser tests with installed stable browsers and real page zoom.

Requires the documented loopback app and project geckodriver; writes ignored screenshots.
"""

import base64
import json
import time
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "http://127.0.0.1:8000/"
DRIVER_URL = "http://127.0.0.1:4445"


def chrome():
    with TemporaryDirectory(dir=ROOT / ".local", prefix="chrome-check-") as profile:
        with sync_playwright() as playwright:
            with playwright.chromium.launch_persistent_context(
                profile, channel="chrome", viewport={"width": 1280, "height": 720}
            ) as context:
                page = context.pages[0]
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on(
                    "console",
                    lambda message: (
                        errors.append(message.text) if message.type == "error" else None
                    ),
                )
                print("Stable Chrome", context.browser.version)
                for zoom in (1, 2):
                    page.goto("chrome://settings/appearance")
                    page.locator("select#zoomLevel").select_option(str(zoom))
                    page.goto(BASE_URL)
                    page.wait_for_function("window.htmx !== undefined")
                    page.keyboard.press("Tab")
                    button = page.get_by_role("button", name="Check connection")
                    expect(button).to_be_focused()
                    assert (
                        button.evaluate("el => getComputedStyle(el).outlineStyle")
                        != "none"
                    )
                    page.keyboard.press("Enter")
                    expect(page.get_by_role("status")).to_have_text(
                        "Connection checked successfully."
                    )
                    metrics = page.evaluate(
                        "({width:innerWidth,height:innerHeight,dpr:devicePixelRatio,overflow:document.documentElement.scrollWidth > innerWidth})"
                    )
                    assert not metrics["overflow"]
                    assert metrics["width"] == 1280 // zoom
                    assert metrics["height"] == 720 // zoom
                    page.screenshot(
                        path=str(ROOT / f".local/skeleton-chrome-{zoom * 100}.png"),
                        full_page=False,
                    )
                    print(
                        f"Chrome native Page zoom{zoom * 100}%:",
                        metrics,
                        "keyboard/HTMX/focus PASS",
                    )
                assert errors == []


def webdriver(method, path, data=None):
    request = urllib.request.Request(
        DRIVER_URL + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["value"]


def firefox():
    created = webdriver(
        "POST",
        "/session",
        {
            "capabilities": {
                "alwaysMatch": {
                    "browserName": "firefox",
                    "moz:firefoxOptions": {
                        "binary": "/Applications/Firefox.app/Contents/MacOS/firefox",
                        "args": ["-headless"],
                    },
                }
            }
        },
    )
    session = "/session/" + created["sessionId"]
    print("Stable Firefox", created["capabilities"]["browserVersion"])

    def execute(script):
        return webdriver(
            "POST", session + "/execute/sync", {"script": script, "args": []}
        )

    def key(value):
        webdriver(
            "POST",
            session + "/actions",
            {
                "actions": [
                    {
                        "type": "key",
                        "id": "keyboard",
                        "actions": [
                            {"type": "keyDown", "value": value},
                            {"type": "keyUp", "value": value},
                        ],
                    }
                ]
            },
        )

    try:
        webdriver("POST", session + "/window/rect", {"width": 1280, "height": 812})
        webdriver("POST", session + "/url", {"url": BASE_URL})
        dimensions = execute("return {width:innerWidth,height:innerHeight}")
        rect = webdriver("GET", session + "/window/rect")
        webdriver(
            "POST",
            session + "/window/rect",
            {
                "width": rect["width"] + 1280 - dimensions["width"],
                "height": rect["height"] + 720 - dimensions["height"],
            },
        )
        for zoom in (1, 2):
            webdriver("POST", session + "/url", {"url": BASE_URL})
            webdriver("POST", session + "/moz/context", {"context": "chrome"})
            actual = execute(
                f"window.gBrowser.selectedBrowser.browsingContext.fullZoom = {zoom}; return window.gBrowser.selectedBrowser.browsingContext.fullZoom;"
            )
            assert actual == zoom
            webdriver("POST", session + "/moz/context", {"context": "content"})
            deadline = time.monotonic() + 5
            while not execute("return window.htmx !== undefined"):
                assert time.monotonic() < deadline
                time.sleep(0.05)
            key("\ue004")  # Tab
            assert (
                execute("return document.activeElement.textContent")
                == "Check connection"
            )
            assert (
                execute("return getComputedStyle(document.activeElement).outlineStyle")
                != "none"
            )
            key("\ue007")  # Enter
            deadline = time.monotonic() + 5
            while (
                execute(
                    "return document.querySelector('#smoke-status').textContent.trim()"
                )
                != "Connection checked successfully."
            ):
                assert time.monotonic() < deadline
                time.sleep(0.05)
            metrics = execute(
                "return {width:innerWidth,height:innerHeight,dpr:devicePixelRatio,overflow:document.documentElement.scrollWidth > innerWidth}"
            )
            assert not metrics["overflow"]
            assert metrics["width"] == 1280 // zoom
            assert metrics["height"] == 720 // zoom
            encoded = webdriver("GET", session + "/screenshot")
            (ROOT / f".local/skeleton-firefox-{zoom * 100}.png").write_bytes(
                base64.b64decode(encoded)
            )
            print(
                f"Firefox native fullZoom{actual * 100}%:",
                metrics,
                "keyboard/HTMX/focus PASS",
            )
    finally:
        webdriver("DELETE", session)


if __name__ == "__main__":
    chrome()
    firefox()
