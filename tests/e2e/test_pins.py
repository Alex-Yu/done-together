import re

from playwright.sync_api import expect
from test_households import PASSWORD, register_verify_login


def expect_locked_board(page):
    # Snapshot polling can append a recovery explanation to the locked caption.
    # Verify the actual locked board and recoverable controls, not one copy variant.
    expect(page.locator("#parent-lock-status")).to_have_text(
        re.compile(r"^Parent controls locked\.")
    )
    expect(page.locator(".child-columns")).to_be_visible()
    unlock = page.get_by_role("button", name="Unlock parent controls", exact=True)
    expect(unlock).to_be_visible()
    expect(unlock).to_be_enabled()
    expect(
        page.get_by_role("link", name="Manage household settings", exact=True)
    ).to_have_count(0)


def test_parent_pin_child_management_lock_and_reset(
    page, live_server, mailoutbox, browser_name
):
    register_verify_login(
        page, live_server, mailoutbox, f"pin-{browser_name}@example.test"
    )
    page.get_by_role("link", name="Household settings").click()
    page.get_by_role("button", name="Create household").click()
    page.get_by_role("link", name="Set or reset your own parent PIN").click()
    page.locator("[name=password]").fill(PASSWORD)
    page.locator("[name=pin]").fill("0007")
    page.get_by_role("button", name="Save parent PIN").click()
    expect_locked_board(page)
    page.locator("[name=pin]").fill("0007")
    page.get_by_role("button", name="Unlock parent controls").click()
    page.get_by_role("link", name="Manage household settings").click()
    page.get_by_role("link", name="Add child", exact=True).click()
    page.get_by_label("Child display name:", exact=True).fill("Aster")
    page.get_by_label("Child PIN:", exact=True).fill("0123")
    page.get_by_role("button", name="Save child").click()
    page.get_by_role("link", name="Edit name", exact=True).click()
    page.get_by_label("Child display name:", exact=True).fill("Birch")
    page.get_by_role("button", name="Save child").click()
    page.get_by_role("link", name="Reset child PIN", exact=True).click()
    page.get_by_label("New child PIN:", exact=True).fill("0456")
    page.get_by_role("button", name="Save child").click()
    page.get_by_role("link", name="Return to board", exact=True).click()
    page.get_by_role("button", name="Lock parent controls").click()
    expect(page.get_by_text("Birch", exact=True)).to_be_visible()
    expect_locked_board(page)
    page.get_by_role("link", name="Set or reset your own parent PIN").click()
    page.locator("[name=password]").fill(PASSWORD)
    page.locator("[name=pin]").fill("0789")
    page.get_by_role("button", name="Save parent PIN").click()
    page.locator("[name=pin]").fill("0007")
    page.get_by_role("button", name="Unlock parent controls").click()
    expect(
        page.get_by_text(
            "Unable to unlock. Check the selected parent and PIN or try again in five minutes."
        )
    ).to_be_visible()
    page.locator("[name=pin]").fill("0789")
    page.get_by_role("button", name="Unlock parent controls").click()
    expect(page.get_by_text("Parent controls unlocked.", exact=True)).to_be_visible()
    expect(page.get_by_text("Birch", exact=True)).to_be_visible()
