import re
from urllib.parse import urlsplit

from playwright.sync_api import expect

PASSWORD = "Local-Synthetic-7392!"


def captured_path(mailoutbox, fragment):
    links = re.findall(r"https?://[^\s]+", mailoutbox[-1].body)
    return next(urlsplit(url).path for url in links if fragment in url)


def register_verify_login(page, live_server, mailoutbox, email):
    page.goto(live_server.url + "/accounts/signup/")
    page.get_by_label("Email:", exact=True).fill(email)
    page.get_by_label("Password:", exact=True).fill(PASSWORD)
    page.get_by_label("Password (again):", exact=True).fill(PASSWORD)
    page.get_by_role("button", name="Create account", exact=True).click()
    expect(page.get_by_role("heading", name="Check your email")).to_be_visible()
    page.goto(live_server.url + captured_path(mailoutbox, "confirm-email/"))
    page.get_by_role("button", name="Verify email").click()
    page.get_by_label("Email:", exact=True).fill(email)
    page.get_by_label("Password:", exact=True).fill(PASSWORD)
    page.get_by_role("button", name="Sign in", exact=True).click()


def test_household_timezone_invite_new_parent_join_and_other_computer(
    page, live_server, mailoutbox, browser_name
):
    browser = page.context.browser
    creator_context = browser.new_context(
        timezone_id="Europe/Warsaw", viewport={"width": 1280, "height": 720}
    )
    recipient_context = browser.new_context(
        timezone_id="America/New_York", viewport={"width": 1280, "height": 720}
    )
    try:
        creator = creator_context.new_page()
        recipient = recipient_context.new_page()
        creator.set_default_timeout(5000)
        recipient.set_default_timeout(5000)
        errors = []
        for tab in (creator, recipient):
            tab.on("pageerror", lambda error: errors.append(str(error)))
            tab.on(
                "console",
                lambda message: (
                    errors.append(message.text) if message.type == "error" else None
                ),
            )
        first = f"house-first-{browser_name}@example.test"
        second = f"house-second-{browser_name}@example.test"
        register_verify_login(creator, live_server, mailoutbox, first)
        creator.get_by_role("link", name="Household settings").click()
        expect(
            creator.get_by_role("heading", name="Create your household")
        ).to_be_visible()
        zone = creator.get_by_label("Scheduling timezone:", exact=True)
        expect(zone).to_have_value("Europe/Warsaw")
        for _ in range(6):
            creator.keyboard.press("Tab")
            if zone.evaluate("el=>el===document.activeElement"):
                break
        expect(zone).to_be_focused()
        assert zone.evaluate("el=>getComputedStyle(el).outlineStyle") != "none"
        creator.keyboard.press("Tab")
        creator.keyboard.press("Enter")
        expect(
            creator.get_by_role("heading", name="Household settings")
        ).to_be_visible()
        creator.get_by_label("Second parent’s email:", exact=True).fill(second)
        creator.get_by_role("button", name="Send invitation").click()
        expect(creator.get_by_role("status")).to_have_text(
            "Invitation email sent. The link expires in seven days."
        )
        private_path = captured_path(mailoutbox, "households/invitations/")
        # Open invitation before account creation; pending flow survives registration.
        recipient.goto(live_server.url + private_path)
        expect(
            recipient.get_by_role("heading", name="Sign in", exact=True)
        ).to_be_visible()
        register_verify_login(recipient, live_server, mailoutbox, second)
        expect(
            recipient.get_by_role("heading", name="Join the household")
        ).to_be_visible()
        recipient.get_by_role("button", name="Join household").click()
        expect(
            recipient.get_by_role("heading", name="Household settings")
        ).to_be_visible()
        expect(recipient.get_by_text(first, exact=True)).to_be_visible()
        expect(recipient.get_by_text(second, exact=True)).to_be_visible()
        expect(recipient.get_by_text("Europe/Warsaw", exact=True)).to_be_visible()
        assert recipient.locator('select[name="timezone"]').count() == 0
        recipient.reload()
        expect(recipient.get_by_text("Europe/Warsaw", exact=True)).to_be_visible()
        creator.reload()
        expect(creator.get_by_text(second, exact=True).first).to_be_visible()
        recipient.goto(live_server.url + private_path)
        expect(
            recipient.get_by_role("heading", name="Invitation unavailable")
        ).to_be_visible()
        # Expected explicit400 replay response is not a script failure.
        assert not [error for error in errors if "400 (Bad Request)" not in error]
    finally:
        creator_context.close()
        recipient_context.close()
