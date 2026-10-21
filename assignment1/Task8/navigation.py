#Core Navigation & Web Automation

import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_core_navigation():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False,slow_mo=1000)

        try:
            page = await browser.new_page()

            # 1. Navigate to the application
            await page.goto("https://www.saucedemo.com/")

            # 2. Validate URL and page title
            await expect(page).to_have_url(
                "https://www.saucedemo.com/"
            )
            await expect(page).to_have_title("Swag Labs")

            # 3 and 4. Locate fields and fill login credentials
            await expect(page.locator("#user-name")).to_be_visible()
            await expect(page.locator("#password")).to_be_visible()

            await page.locator("#user-name").fill("standard_user")
            await page.locator("#password").fill("secret_sauce")

            # 5. Click Login
            await page.locator("#login-button").click()

            # 6. Verify successful login
            await expect(page).to_have_url(
                "https://www.saucedemo.com/inventory.html"
            )
            await expect(page.locator(".inventory_list")).to_be_visible()

            # 7. Navigate to a product
            await page.locator("#item_4_title_link").click()

            await expect(page).to_have_url(
                "https://www.saucedemo.com/inventory-item.html?id=4"
            )
            await expect(
                page.locator(".inventory_details_container")
            ).to_be_visible()

            # 8. Go back to the products page
            await page.go_back()
            await expect(page.locator(".inventory_list")).to_be_visible()

            # Go forward to the product details page
            await page.go_forward()
            await expect(
                page.locator(".inventory_details_container")
            ).to_be_visible()

            # Reload the product details page
            await page.reload()
            await expect(
                page.locator(".inventory_details_container")
            ).to_be_visible()

        finally:
            # Close the browser
            await browser.close()