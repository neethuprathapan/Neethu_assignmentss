# Environment Files & Environment-Specific Variables

import pytest
from playwright.sync_api import sync_playwright, expect


# Environment configurations
ENVIRONMENTS = [
    ("DEV", "https://demowebshop.tricentis.com"),
    ("QA", "https://www.amazon.in/"),
    ("STAGING", "https://www.saucedemo.com/"),
]

# used parametrize to run the 3 environment together
@pytest.mark.parametrize("environment, website_url",ENVIRONMENTS)

def test_environment_url(environment, website_url):
    print(f"\nSelected environment: {environment}")
    print(f"Website URL: {website_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=1000)

        try:
            page = browser.new_page()
            page.goto(website_url)

            expect(page.locator("body")).to_be_visible()
            assert page.url.startswith(website_url)

        finally:
            browser.close()