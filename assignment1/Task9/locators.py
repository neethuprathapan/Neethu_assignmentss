#Locator Strategies


import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_locators():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)

        try:
            page = await browser.new_page()

            # 1. CSS selector
            await page.goto("https://www.saucedemo.com/")
            username = page.locator("#user-name")
            await username.fill("standard_user")
            await expect(username).to_have_value("standard_user")

            # 2. XPath
            password = page.locator('xpath=//*[@id="password"]')
            await password.fill("secret_sauce")
            await expect(password).to_have_value("secret_sauce")

            # 3. Visible text
            await page.get_by_text("Login", exact=True).click()
            await expect(page.locator(".inventory_list")).to_be_visible()

            # 4. get_by_role()
            backpack = page.get_by_role(
                "button",
                name="View details for Sauce Labs Backpack",
                exact=True
            ).last
            await expect(backpack).to_be_visible()
            await backpack.click()
            await expect(
                page.locator(".inventory_details_name")
            ).to_have_text("Sauce Labs Backpack")

            # 5. get_by_label() using Google
            await page.goto("https://www.google.com/")
            search = page.get_by_label("Search").nth(1)
            await search.fill("Playwright Python")
            await expect(search).to_have_value("Playwright Python")

            print("All locator strategies tested successfully!")

        finally:
            await browser.close()

