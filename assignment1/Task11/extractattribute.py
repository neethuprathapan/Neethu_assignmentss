#Extracting Text and Attributes



import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_extracting_text_and_attributes():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)

        try:
            page = await browser.new_page()
            await page.goto("https://www.saucedemo.com/")

            # 1. Locate a heading and retrieve its text
            heading = page.locator(".login_logo")
            heading_text = await heading.inner_text()

            print("Heading text:", heading_text)
            assert heading_text == "Swag Labs"

            # 2. Retrieve inner text from a container with multiple elements
            container = page.locator(".login_wrapper")
            container_text = await container.inner_text()

            print("Container text:", container_text)
            assert "standard_user" in container_text
            assert "secret_sauce" in container_text

            # 3. Retrieve an input field's value
            username = page.locator("#user-name")
            await username.fill("standard_user")
            username_value = await username.input_value()

            print("\n Username value:", username_value)
            assert username_value == "standard_user"

            # 4. Read two HTML attributes
            placeholder = await username.get_attribute("placeholder")
            input_class = await username.get_attribute("class")

            print("\nPlaceholder:", placeholder)
            print("\nInput class:", input_class)

            assert placeholder == "Username"
            assert input_class is not None

            # 6. Validate important values
            await expect(heading).to_have_text("Swag Labs")
            await expect(username).to_have_value("standard_user")

            print("\nAll checks passed!")

        finally:
            await browser.close()