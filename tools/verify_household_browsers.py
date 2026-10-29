"""Synthetic installed-browser household journeys/native zoom; requires app+Mailpit+driver.

Seeded verified accounts are local test fixtures, not a product verification bypass.
Runtime credentials remain in ignored0600 .local/household-browser-fixtures.json.
"""

import argparse
import base64
import json
import os
import secrets
import sys
import time
from tempfile import TemporaryDirectory

from playwright.sync_api import sync_playwright
from verify_account_mail import capture_path
from verify_skeleton_browsers import BASE_URL, ROOT, webdriver

FIXTURES = ROOT / ".local/household-browser-fixtures.json"
sys.path.insert(0, str(ROOT))


def fixtures():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    import django

    django.setup()
    from allauth.account.models import EmailAddress
    from django.contrib.auth import get_user_model

    records = []
    for engine in ("chrome", "firefox"):
        for zoom in (1, 2):
            record = {
                "engine": engine,
                "zoom": zoom,
                "password": "Local-check-" + secrets.token_urlsafe(24),
            }
            for kind in ("creator", "recipient"):
                email = f"{engine}-{kind}-{secrets.token_hex(5)}@example.test"
                user = get_user_model().objects.create_user(
                    username=email, email=email, password=record["password"]
                )
                EmailAddress.objects.create(
                    user=user, email=email, verified=True, primary=True
                )
                record[kind] = email
            records.append(record)
    FIXTURES.write_text(json.dumps(records))
    FIXTURES.chmod(0o600)
    return records


class Chrome:
    def __init__(self, playwright, profile, zoom):
        self.context = playwright.chromium.launch_persistent_context(
            profile,
            channel="chrome",
            viewport={"width": 1280, "height": 720},
            timezone_id="Europe/Warsaw",
        )
        self.page = self.context.pages[0]
        self.page.set_default_timeout(5000)
        self.page.goto("chrome://settings/appearance")
        self.page.locator("select#zoomLevel").select_option(str(zoom))
        self.version = self.context.browser.version
        self.zoom = zoom

    def execute(self, script):
        return self.page.evaluate(script)

    def goto(self, path):
        self.page.goto(BASE_URL.rstrip("/") + path)

    def press(self, key):
        if key == "Enter":
            with self.page.expect_navigation(wait_until="load"):
                self.page.keyboard.press(key)
        else:
            self.page.keyboard.press(key)

    def fill(self, name, text):
        self.page.locator(f'[name="{name}"]').fill(text)

    def click(self, text):
        with self.page.expect_navigation(wait_until="load"):
            self.page.get_by_role("button", name=text, exact=True).click()

    def apply_zoom(self):
        pass

    def screenshot(self, path):
        self.page.screenshot(path=str(path))

    def close(self):
        self.context.close()


class Firefox:
    def __init__(self, zoom):
        result = webdriver(
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
        self.session = "/session/" + result["sessionId"]
        self.version = result["capabilities"]["browserVersion"]
        self.zoom = zoom
        webdriver("POST", self.session + "/window/rect", {"width": 1280, "height": 812})
        self.goto("/")
        dimensions = self.execute("({width:innerWidth,height:innerHeight})")
        rect = webdriver("GET", self.session + "/window/rect")
        webdriver(
            "POST",
            self.session + "/window/rect",
            {
                "width": rect["width"] + 1280 - dimensions["width"],
                "height": rect["height"] + 720 - dimensions["height"],
            },
        )

    def execute(self, script):
        return webdriver(
            "POST",
            self.session + "/execute/sync",
            {"script": "return " + script, "args": []},
        )

    def goto(self, path):
        webdriver("POST", self.session + "/url", {"url": BASE_URL.rstrip("/") + path})

    def press(self, key):
        value = {
            "Tab": "\ue004",
            "Space": "\ue00d",
            "Enter": "\ue007",
            "ArrowUp": "\ue013",
            "ArrowDown": "\ue015",
        }[key]
        webdriver(
            "POST",
            self.session + "/actions",
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

    def fill(self, name, text):
        element = webdriver(
            "POST",
            self.session + "/element",
            {"using": "css selector", "value": f'[name="{name}"]'},
        )
        identity = element["element-6066-11e4-a52e-4f735466cecf"]
        webdriver("POST", self.session + f"/element/{identity}/clear", {})
        webdriver("POST", self.session + f"/element/{identity}/value", {"text": text})

    def click(self, text):
        element = self.execute(
            "[...document.querySelectorAll('button')].find(el=>el.textContent.trim()==="
            + json.dumps(text)
            + ")"
        )
        identity = element["element-6066-11e4-a52e-4f735466cecf"]
        webdriver("POST", self.session + f"/element/{identity}/click", {})

    def apply_zoom(self):
        try:
            webdriver("POST", self.session + "/moz/context", {"context": "chrome"})
            value = webdriver(
                "POST",
                self.session + "/execute/sync",
                {
                    "script": f"window.gBrowser.selectedBrowser.browsingContext.fullZoom={self.zoom};return window.gBrowser.selectedBrowser.browsingContext.fullZoom;",
                    "args": [],
                },
            )
            assert value == self.zoom
        finally:
            webdriver("POST", self.session + "/moz/context", {"context": "content"})

    def screenshot(self, path):
        path.write_bytes(
            base64.b64decode(webdriver("GET", self.session + "/screenshot"))
        )

    def close(self):
        webdriver("DELETE", self.session)


def wait_for(ui, expression, expected):
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            matched = ui.execute(expression) == expected
        except Exception:
            # Native navigation can replace the execution context between polls.
            matched = False
        if matched:
            # Zoom/setup errors are not navigation races. Surface them directly.
            ui.apply_zoom()
            return
        time.sleep(0.05)
    raise AssertionError("Browser navigation/status did not settle")


def wait_heading(ui, text):
    wait_for(ui, "document.querySelector('h1')?.textContent.trim()", text)


def tab_to(ui, name=None, button=False):
    for _ in range(15):
        ui.press("Tab")
        if (
            ui.execute("document.activeElement.tagName") == "BUTTON"
            if button
            else ui.execute("document.activeElement.name") == name
        ):
            assert (
                ui.execute("getComputedStyle(document.activeElement).outlineStyle")
                != "none"
            )
            if not button:
                assert ui.execute("document.activeElement.labels.length") > 0
            return
    raise AssertionError("Keyboard target not reached")


def signin(ui, email, password):
    ui.goto("/accounts/login/")
    wait_heading(ui, "Sign in")
    ui.fill("login", email)
    ui.fill("password", password)
    ui.click("Sign in")
    wait_heading(ui, "Done Together")


def setup_parent_and_settings(ui, password, pin="2468"):
    wait_heading(ui, "Done Together")
    path = ui.execute(
        "[...document.querySelectorAll('a')].find(el=>el.getAttribute('href').endsWith('/parent-pin/')).getAttribute('href')"
    )
    ui.goto(path)
    wait_heading(ui, "Set or reset your parent PIN")
    ui.fill("password", password)
    ui.fill("pin", pin)
    ui.click("Save parent PIN")
    wait_heading(ui, "Done Together")
    ui.fill("pin", pin)
    ui.click("Unlock parent controls")
    wait_for(
        ui,
        "document.getElementById('parent-lock-status').textContent.trim()",
        "Parent controls unlocked.",
    )
    path = ui.execute(
        "[...document.querySelectorAll('a')].find(el=>el.textContent.trim()==='Manage household settings').getAttribute('href')"
    )
    ui.goto(path)
    wait_heading(ui, "Household settings")


def open_existing_settings(ui, pin="2468"):
    wait_heading(ui, "Done Together")
    ui.fill("pin", pin)
    ui.click("Unlock parent controls")
    wait_for(
        ui,
        "document.getElementById('parent-lock-status').textContent.trim()",
        "Parent controls unlocked.",
    )
    path = ui.execute(
        "[...document.querySelectorAll('a')].find(el=>el.textContent.trim()==='Manage household settings').getAttribute('href')"
    )
    ui.goto(path)
    wait_heading(ui, "Household settings")


def journey(ui, record):
    signin(ui, record["creator"], record["password"])
    ui.goto("/households/")
    wait_heading(ui, "Create your household")
    zone = ui.execute("document.querySelector('[name=timezone]').value")
    assert zone == ui.execute("Intl.DateTimeFormat().resolvedOptions().timeZone")
    tab_to(ui, "timezone")
    ui.press("Tab")
    ui.press("Enter")
    setup_parent_and_settings(ui, record["password"])
    tab_to(ui, "email")
    ui.fill("email", record["recipient"])
    ui.press("Tab")
    ui.press("Enter")
    wait_heading(ui, "Household settings")
    wait_for(ui, "document.body.textContent.includes('Invitation email sent.')", True)
    private_path = capture_path(record["recipient"], "households/invitations/")
    ui.goto("/accounts/logout/")
    ui.click("Sign out")
    wait_heading(ui, "Sign in")
    signin(ui, record["recipient"], record["password"])
    ui.goto(private_path)
    wait_heading(ui, "Join the household")
    tab_to(ui, button=True)
    ui.press("Enter")
    setup_parent_and_settings(ui, record["password"])
    assert record["creator"] in ui.execute("document.body.textContent")
    assert zone in ui.execute("document.body.textContent")
    assert ui.execute("document.querySelector('[name=timezone]')===null")
    tab_to(ui, "email")
    ui.fill("email", "third@example.test")
    ui.press("Tab")
    ui.press("Enter")
    wait_heading(ui, "Household settings")
    wait_for(
        ui,
        "document.body.textContent.includes('This household already has two parents.')",
        True,
    )
    metrics = ui.execute(
        "({width:innerWidth,height:innerHeight,dpr:devicePixelRatio,overflow:document.documentElement.scrollWidth>innerWidth})"
    )
    assert metrics["width"] == 1280 // record["zoom"] and not metrics["overflow"]
    ui.screenshot(
        ROOT / f".local/household-{record['engine']}-{record['zoom'] * 100}.png"
    )
    ui.goto(private_path)
    wait_heading(ui, "Invitation unavailable")
    ui.screenshot(
        ROOT / f".local/household-{record['engine']}-{record['zoom'] * 100}-invalid.png"
    )
    record["timezone"] = zone
    print(
        record["engine"],
        ui.version,
        f"native{record['zoom'] * 100}%",
        metrics,
        "create/invite/realSMTP/join/keyboard/errors PASS",
    )


def run(revisit):
    records = json.loads(FIXTURES.read_text()) if revisit else fixtures()
    with sync_playwright() as playwright:
        for record in records:
            with TemporaryDirectory(
                dir=ROOT / ".local", prefix="household-chrome-"
            ) as profile:
                ui = (
                    Chrome(playwright, profile, record["zoom"])
                    if record["engine"] == "chrome"
                    else Firefox(record["zoom"])
                )
                try:
                    if revisit:
                        signin(ui, record["recipient"], record["password"])
                        ui.goto("/households/")
                        open_existing_settings(ui)
                        assert record["creator"] in ui.execute(
                            "document.body.textContent"
                        )
                        assert record["timezone"] in ui.execute(
                            "document.body.textContent"
                        )
                    else:
                        journey(ui, record)
                finally:
                    ui.close()
        if not revisit:
            FIXTURES.write_text(json.dumps(records))
            FIXTURES.chmod(0o600)
    print(
        "Household persisted state after server restart: PASS"
        if revisit
        else "All installed-browser household journeys: PASS"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--revisit", action="store_true")
    try:
        run(parser.parse_args().revisit)
    except Exception as error:
        message = str(error)
        if FIXTURES.exists():
            for record in json.loads(FIXTURES.read_text()):
                message = message.replace(record["password"], "[redacted]")
        from accounts.privacy import AccountLogFilter

        for pattern, replacement in AccountLogFilter.patterns:
            message = pattern.sub(replacement, message)
        raise SystemExit(
            f"Household browser check failed ({type(error).__name__}): {message[:1200]}"
        ) from None
