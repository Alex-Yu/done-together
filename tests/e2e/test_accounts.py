import re
from urllib.parse import urlsplit

from playwright.sync_api import expect


def captured_path(mailoutbox, fragment):
    links = re.findall(r"https?://[^\s]+", mailoutbox[-1].body)
    return next(urlsplit(url).path for url in links if fragment in url)


def test_parent_registration_verification_recovery_and_signout(
    page, live_server, mailoutbox, browser_name
):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on(
        "console",
        lambda message: (
            errors.append(message.text) if message.type == "error" else None
        ),
    )
    email = f"browser-{browser_name}@example.test"
    password = "River-Cloud-4829!"
    replacement = "Amber-Mountain-4932!"
    page.goto(live_server.url + "/accounts/signup/")
    page.get_by_label("Email:", exact=True).fill(email)
    page.get_by_label("Password:", exact=True).fill(password)
    page.get_by_label("Password (again):", exact=True).fill(password)
    page.get_by_role("button", name="Create account", exact=True).click()
    expect(page.get_by_role("heading", name="Check your email")).to_be_visible()
    page.goto(live_server.url + captured_path(mailoutbox, "confirm-email/"))
    page.get_by_role("button", name="Verify email").click()
    page.get_by_label("Email:", exact=True).fill(email)
    page.get_by_label("Password:", exact=True).fill(password)
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("link", name="Sign out")).to_be_visible()
    page.reload()
    expect(page.get_by_role("link", name="Sign out")).to_be_visible()
    page.get_by_role("link", name="Sign out").click()
    page.get_by_role("button", name="Sign out").click()
    page.goto(live_server.url + "/accounts/password/reset/")
    page.get_by_label("Email:", exact=True).fill(email)
    page.get_by_role("button", name="Send recovery email").click()
    expect(page.get_by_role("heading", name="Check your email")).to_be_visible()
    page.goto(live_server.url + captured_path(mailoutbox, "password/reset/key/"))
    page.get_by_label("New Password:", exact=True).fill(replacement)
    page.get_by_label("New Password (again):", exact=True).fill(replacement)
    page.get_by_role("button", name="Save new password").click()
    expect(page.get_by_role("heading", name="Password updated")).to_be_visible()
    page.get_by_role("link", name="Sign in", exact=True).last.click()
    page.get_by_label("Email:", exact=True).fill(email)
    page.get_by_label("Password:", exact=True).fill(password)
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(
        page.get_by_text(
            "Unable to sign in. Check your details or try again in five minutes."
        )
    ).to_be_visible()
    page.get_by_label("Password:", exact=True).fill(replacement)
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("link", name="Sign out")).to_be_visible()
    assert errors == []
