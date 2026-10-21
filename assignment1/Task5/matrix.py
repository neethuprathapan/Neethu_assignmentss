#Browser Matrix Execution

from playwright.sync_api import sync_playwright, expect


def test_home_page(browser_type_name):
    with sync_playwright() as p:
        # used getattr so i can run all 3, selecting Chromium, Firefox, and WebKit dynamically.
        browser_type = getattr(p, browser_type_name)
        browser = browser_type.launch(headless=False,slow_mo=1000)

        try:
            page = browser.new_page()
            page.goto("https://www.saucedemo.com/")
            expect(page).to_have_title("Swag Labs")

        finally:
            browser.close()