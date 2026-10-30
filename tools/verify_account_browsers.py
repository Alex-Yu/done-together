"""Installed stable-browser account keyboard/validation checks at native100/200% zoom."""

import base64
import time
from tempfile import TemporaryDirectory

from playwright.sync_api import expect, sync_playwright
from verify_skeleton_browsers import BASE_URL, ROOT, webdriver


def chrome():
    with TemporaryDirectory(dir=ROOT / ".local", prefix="account-chrome-") as profile:
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
                for zoom in (1, 2):
                    page.goto("chrome://settings/appearance")
                    page.locator("select#zoomLevel").select_option(str(zoom))
                    page.goto(BASE_URL + "accounts/login/")
                    for _ in range(10):
                        page.keyboard.press("Tab")
                        if page.get_by_label("Email:", exact=True).evaluate(
                            "el=>el===document.activeElement"
                        ):
                            break
                    expect(page.get_by_label("Email:", exact=True)).to_be_focused()
                    assert (
                        page.get_by_label("Email:", exact=True).evaluate(
                            "el=>getComputedStyle(el).outlineStyle"
                        )
                        != "none"
                    )
                    page.keyboard.type("stable-chrome-unknown@example.test")
                    page.keyboard.press("Tab")
                    expect(page.get_by_label("Password:", exact=True)).to_be_focused()
                    page.keyboard.type("Synthetic-invalid-password!")
                    for _ in range(10):
                        page.keyboard.press("Tab")
                        if page.get_by_role(
                            "button", name="Sign in", exact=True
                        ).evaluate("el=>el===document.activeElement"):
                            break
                    expect(
                        page.get_by_role("button", name="Sign in", exact=True)
                    ).to_be_focused()
                    page.keyboard.press("Enter")
                    expect(
                        page.get_by_text(
                            "Unable to sign in. Check your details or try again in five minutes."
                        )
                    ).to_be_visible()
                    assert (
                        page.get_by_label("Password:", exact=True).input_value() == ""
                    )
                    metrics = page.evaluate(
                        "({width:innerWidth,height:innerHeight,dpr:devicePixelRatio,overflow:document.documentElement.scrollWidth>innerWidth})"
                    )
                    assert metrics["width"] == 1280 // zoom and not metrics["overflow"]
                    page.get_by_label("Email:", exact=True).focus()
                    page.screenshot(
                        path=str(ROOT / f".local/account-chrome-{zoom * 100}.png")
                    )
                    print(
                        "Stable Chrome",
                        context.browser.version,
                        f"native{zoom * 100}%",
                        metrics,
                        "keyboard/labeled fields/validation/privacy PASS",
                    )
                assert not errors


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

    def fill(selector, text):
        element = webdriver(
            "POST", session + "/element", {"using": "css selector", "value": selector}
        )
        identity = element["element-6066-11e4-a52e-4f735466cecf"]
        webdriver("POST", session + f"/element/{identity}/value", {"text": text})

    try:
        webdriver("POST", session + "/window/rect", {"width": 1280, "height": 812})
        webdriver("POST", session + "/url", {"url": BASE_URL + "accounts/login/"})
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
            webdriver("POST", session + "/url", {"url": BASE_URL + "accounts/login/"})
            webdriver("POST", session + "/moz/context", {"context": "chrome"})
            assert (
                execute(
                    f"window.gBrowser.selectedBrowser.browsingContext.fullZoom={zoom};return window.gBrowser.selectedBrowser.browsingContext.fullZoom;"
                )
                == zoom
            )
            webdriver("POST", session + "/moz/context", {"context": "content"})
            for _ in range(10):
                key("\ue004")
                if execute("return document.activeElement.name") == "login":
                    break
            assert execute("return document.activeElement.name") == "login"
            assert (
                execute("return getComputedStyle(document.activeElement).outlineStyle")
                != "none"
            )
            assert execute("return document.activeElement.labels.length") > 0
            fill("input[name=login]", "stable-firefox-unknown@example.test")
            key("\ue004")
            assert execute("return document.activeElement.name") == "password"
            assert execute("return document.activeElement.labels.length") > 0
            fill("input[name=password]", "Synthetic-invalid-password!")
            for _ in range(10):
                key("\ue004")
                if execute("return document.activeElement.tagName") == "BUTTON":
                    break
            assert execute("return document.activeElement.tagName") == "BUTTON"
            key("\ue007")
            deadline = time.monotonic() + 5
            while (
                "Unable to sign in. Check your details or try again in five minutes."
                not in execute("return document.body.textContent")
            ):
                assert time.monotonic() < deadline
                time.sleep(0.05)
            assert (
                execute("return document.querySelector('input[name=password]').value")
                == ""
            )
            # Navigation resets native zoom; reapply for error-page layout observation.
            webdriver("POST", session + "/moz/context", {"context": "chrome"})
            execute(f"window.gBrowser.selectedBrowser.browsingContext.fullZoom={zoom}")
            webdriver("POST", session + "/moz/context", {"context": "content"})
            metrics = execute(
                "return {width:innerWidth,height:innerHeight,dpr:devicePixelRatio,overflow:document.documentElement.scrollWidth>innerWidth}"
            )
            assert metrics["width"] == 1280 // zoom and not metrics["overflow"]
            execute("document.querySelector('input[name=login]').focus()")
            image = webdriver("GET", session + "/screenshot")
            (ROOT / f".local/account-firefox-{zoom * 100}.png").write_bytes(
                base64.b64decode(image)
            )
            print(
                "Stable Firefox",
                created["capabilities"]["browserVersion"],
                f"native{zoom * 100}%",
                metrics,
                "keyboard/labeled fields/validation/privacy PASS",
            )
    finally:
        webdriver("DELETE", session)


if __name__ == "__main__":
    chrome()
    firefox()
