#Built-in Waits & Page Load States

import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
async def test_waits():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Open website and wait for page to load
        await page.goto("https://www.saucedemo.com/", wait_until="domcontentloaded")

        # 2. Wait for username field
        username = page.locator("#user-name")
        await username.wait_for(state="visible")

        # 3. Login
        await username.fill("standard_user")
        await page.locator("#password").fill("secret_sauce")
        await page.locator("#login-button").click()

        # 4. Wait for URL to change
        await page.wait_for_url("**/inventory.html")

        # 5. Verify products are visible
        await expect(page.locator(".inventory_list")).to_be_visible()

        print("Login successful!")

        await browser.close()