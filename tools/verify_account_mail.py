"""Synthetic real-SMTP account journey; --revisit proves persistence after restart.

Requires loopback app/Mailpit. Credentials stay in ignored mode0600 local fixture.
"""

import argparse
import json
import re
import secrets
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "http://127.0.0.1:8000"
FIXTURE = ROOT / ".local/account-mailpit-fixture.json"


def capture_path(email, fragment):
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        with urllib.request.urlopen(
            "http://127.0.0.1:8025/api/v1/messages"
        ) as response:
            messages = json.load(response)["messages"]
        for message in messages:
            if not any(to["Address"] == email for to in message["To"]):
                continue
            with urllib.request.urlopen(
                "http://127.0.0.1:8025/api/v1/message/" + message["ID"]
            ) as response:
                body = json.load(response)["Text"]
            links = re.findall(r"https?://[^\s]+", body)
            for link in links:
                if fragment in link:
                    return urlsplit(link).path
        time.sleep(0.1)
    raise RuntimeError("Synthetic capture was not received")


def sign_in(page, email, password):
    page.goto(BASE_URL + "/accounts/login/")
    page.get_by_label("Email:", exact=True).fill(email)
    page.get_by_label("Password:", exact=True).fill(password)
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("link", name="Sign out")).to_be_visible()


def run(revisit):
    with sync_playwright() as playwright:
        with playwright.chromium.launch(channel="chrome") as browser:
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.set_default_timeout(5000)
            if revisit:
                data = json.loads(FIXTURE.read_text())
                sign_in(page, data["email"], data["password"])
                page.reload()
                expect(page.get_by_role("link", name="Sign out")).to_be_visible()
                print(
                    "Stored synthetic account survives signout/reload/server restart: PASS"
                )
                return
            email = "account-" + secrets.token_hex(5) + "@example.test"
            password = "Local-check-" + secrets.token_urlsafe(24)
            replacement = "Local-reset-" + secrets.token_urlsafe(24)
            page.goto(BASE_URL + "/accounts/signup/")
            page.get_by_label("Email:", exact=True).fill(email)
            page.get_by_label("Password:", exact=True).fill(password)
            page.get_by_label("Password (again):", exact=True).fill(password)
            page.get_by_role("button", name="Create account", exact=True).click()
            expect(page.get_by_role("heading", name="Check your email")).to_be_visible()
            path = capture_path(email, "confirm-email/")
            page.goto(BASE_URL + path)
            page.get_by_role("button", name="Verify email").click()
            sign_in(page, email, password)
            page.get_by_role("link", name="Sign out").click()
            page.get_by_role("button", name="Sign out").click()
            page.goto(BASE_URL + "/accounts/password/reset/")
            page.get_by_label("Email:", exact=True).fill(email)
            page.get_by_role("button", name="Send recovery email").click()
            expect(page.get_by_role("heading", name="Check your email")).to_be_visible()
            page.goto(BASE_URL + capture_path(email, "password/reset/key/"))
            page.get_by_label("New Password:", exact=True).fill(replacement)
            page.get_by_label("New Password (again):", exact=True).fill(replacement)
            page.get_by_role("button", name="Save new password").click()
            expect(page.get_by_role("heading", name="Password updated")).to_be_visible()
            sign_in(page, email, replacement)
            page.reload()
            expect(page.get_by_role("link", name="Sign out")).to_be_visible()
            page.get_by_role("link", name="Sign out").click()
            page.get_by_role("button", name="Sign out").click()
            FIXTURE.write_text(json.dumps({"email": email, "password": replacement}))
            FIXTURE.chmod(0o600)
            capture = browser.new_page(viewport={"width": 1280, "height": 720})
            capture.goto("http://127.0.0.1:8025/")
            capture.get_by_text(email, exact=False).first.wait_for()
            capture.screenshot(path=str(ROOT / ".local/account-mailpit-capture.png"))
            print(
                "Actual Mailpit verification/recovery capture and installed Chrome account lifecycle: PASS"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--revisit", action="store_true")
    try:
        run(parser.parse_args().revisit)
    except Exception as error:
        # Browser exception call logs can embed private links or fill values.
        raise SystemExit(
            f"Account SMTP/browser check failed ({type(error).__name__}); inspect local service state without printing credentials or links."
        ) from None
