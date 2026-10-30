from playwright.sync_api import expect


def test_landing_local_htmx_and_keyboard_interaction(page, live_server):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on(
        "console",
        lambda message: (
            errors.append(message.text) if message.type == "error" else None
        ),
    )
    page.set_viewport_size({"width": 1280, "height": 720})
    page.goto(live_server.url)
    expect(
        page.get_by_role("heading", name="Done Together", exact=True)
    ).to_be_visible()
    page.wait_for_function("window.htmx !== undefined")
    assert page.locator("script[src]").get_attribute("src").startswith("/static/")
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    button = page.get_by_role("button", name="Check connection")
    expect(button).to_be_focused()
    assert button.evaluate("el => getComputedStyle(el).outlineStyle") != "none"
    page.keyboard.press("Enter")
    expect(page.get_by_role("status")).to_have_text("Connection checked successfully.")
    assert errors == []
