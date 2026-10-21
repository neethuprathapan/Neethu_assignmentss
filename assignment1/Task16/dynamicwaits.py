#Dynamic Waits for SPA Applications

import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
async def test_dynamic_waits():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Open website
        await page.goto("https://www.saucedemo.com/")

        # 2. Login to trigger a page update
        await page.locator("#user-name").fill("standard_user")
        await page.locator("#password").fill("secret_sauce")
        await page.locator("#login-button").click()

        # 3. Wait for the dynamic page update
        await page.wait_for_url("**/inventory.html")

        # 4. Validate the final state
        products = page.locator(".inventory_item")
        await expect(products).to_have_count(6)

        print("Inventory page loaded. Products:", await products.count())

        await browser.close()