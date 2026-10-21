#Timeout Handling & Custom Wait Conditions

import pytest
from playwright.async_api import async_playwright, expect, TimeoutError

@pytest.mark.asyncio
async def test_timeout_handling():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Set default and navigation timeouts
        page.set_default_timeout(5000)
        page.set_default_navigation_timeout(10000)

        await page.goto("https://www.saucedemo.com/")

        # 2. Intentionally wait for a missing element
        try:
            await page.locator("#missing-element").wait_for()
        except TimeoutError:
            print("Timeout: The element was not found within 5 seconds.")

        # 3. Login to trigger a dynamic state
        await page.locator("#user-name").fill("standard_user")
        await page.locator("#password").fill("secret_sauce")
        await page.locator("#login-button").click()

        # 4. Custom wait condition: wait until products appear
        try:
            await expect(page.locator(".inventory_item")).to_have_count(6, timeout=5000)
            print("Success: All 6 products are displayed.")

        except AssertionError:
            raise AssertionError(
                "Custom wait failed: Expected 6 products on the inventory page."
            )

        await browser.close()