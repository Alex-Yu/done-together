from playwright.sync_api import expect
from test_households import PASSWORD, register_verify_login


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
    expect(page.get_by_text("Parent controls locked.", exact=True)).to_be_visible()
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
    expect(page.get_by_text("Parent controls locked.", exact=True)).to_be_visible()
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
