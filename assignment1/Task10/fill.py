#Typing, Filling and Keyboard Actions



import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_typing_and_keyboard_actions():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)

        try:
            page = await browser.new_page()
            await page.goto("https://www.saucedemo.com/")

            # 1. Locate text inputs
            username = page.locator("#user-name")

            # 2. Enter data using fill()
            await username.fill("wrong_user")
            await expect(username).to_have_value("wrong_user")

            # 3. Use press() for a keyboard action
            await username.press("Control+A")
            await username.fill("standard_user")

            # 4. Clear and replace an existing value
            await username.fill("")
            await username.fill("standard_user")

            # 5. Validate the final input values
            await expect(username).to_have_value("standard_user")


            # 6. Demonstrate keyboard shortcut: Control+A
            await username.press("Control+A")
            await username.fill("standard_user")
            await expect(username).to_have_value("standard_user")

            # Press Enter to submit the login form
            password = page.locator("#password")
            await password.fill("secret_sauce")
            await expect(password).to_have_value("secret_sauce")
            await password.press("Enter")
            await expect(page.locator(".inventory_list")).to_be_visible()

            print("All typing and keyboard actions passed!")

        finally:
            await browser.close()