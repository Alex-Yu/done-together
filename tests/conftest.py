import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def page(live_server, transactional_db, browser_name, pytestconfig):
    # Start/stop Playwright within the DB fixture lifetime. Its sync API owns
    # an event loop; Django DB setup/teardown must happen outside that loop.
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, browser_name)
        with browser_type.launch(
            headless=not pytestconfig.getoption("headed")
        ) as browser:
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            page.set_default_timeout(5000)
            yield page
            context.close()
