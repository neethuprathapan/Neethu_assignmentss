#Assertions: expect() and pytest


import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_assertions():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)

        try:
            page = await browser.new_page()
            await page.goto("https://www.saucedemo.com/")

            # 1. Verify page title using expect()
            await expect(page).to_have_title("Swag Labs")

            # 2. Verify URL using expect()
            await expect(page).to_have_url("https://www.saucedemo.com/")

            # 3. Verify element visibility
            heading = page.locator(".login_logo")
            await expect(heading).to_be_visible()

            # 4. Verify element text
            await expect(heading).to_have_text("Swag Labs")

            # 5. Verify input value
            username = page.locator("#user-name")
            await username.fill("standard_user")
            await expect(username).to_have_value("standard_user")

            # 6. Verify an element is enabled
            login_button = page.locator("#login-button")
            await expect(login_button).to_be_enabled()

            # Verify a disabled element
            await username.fill("")
            await expect(username).to_be_enabled()

            # 7. Use pytest assert for a calculated value
            username_value = await username.input_value()
            username_length = len(username_value)

            print("Username length:", username_length)
            assert username_length == 0

            # Login and verify the products page
            await username.fill("standard_user")
            await page.locator("#password").fill("secret_sauce")
            await login_button.click()

            await expect(page.locator(".inventory_list")).to_be_visible()
            await expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

            print("All assertions passed!")

        finally:
            await browser.close()