#Soft Assertions,


import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_soft_assertions():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)

        try:
            page = await browser.new_page()
            await page.goto("https://www.saucedemo.com/")

            failures = []

            # 1. Validate page title
            try:
                await expect(page).to_have_title("Swag Labs")
            except AssertionError:
                failures.append("Page title validation failed")

            # 2. Validate URL
            try:
                await expect(page).to_have_url( "https://www.saucedemo.com/")
            except AssertionError:
                failures.append("URL validation failed")

            # 3. Validate heading visibility
            try:
                await expect(page.locator(".login_logo")).to_be_visible()
            except AssertionError:
                failures.append("Heading visibility validation failed")

            # 4. Validate heading text
            try:
                await expect(page.locator(".login_logo")).to_have_text("Swag Labs")
            except AssertionError:
                failures.append("Heading text validation failed")

            # 5. Validate username field
            try:
                await expect(page.locator("#user-name")).to_be_visible()
            except AssertionError:
                failures.append("Username field validation failed")

            # Report all failures at the end
            if failures:
                pytest.fail("\nSoft assertion failures:\n" + "\n".join(failures))

            print("All soft assertions passed!")

        finally:
            await browser.close()