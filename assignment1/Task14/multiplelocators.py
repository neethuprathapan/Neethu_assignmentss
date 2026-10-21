#Multiple Locators


import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_multiple_locators():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)

        try:
            page = await browser.new_page()
            await page.goto("https://www.saucedemo.com/")

            # Login
            await page.locator("#user-name").fill("standard_user")
            await page.locator("#password").fill("secret_sauce")
            await page.locator("#login-button").click()

            # 1. Find all matching elements using locator()
            products = page.locator(".inventory_item_name")

            # 2. Print the count of matching elements
            count = await products.count()
            print("Number of products:", count)

            # 3. Interact with the first matching element
            first_product = products.first
            print("First product:", await first_product.inner_text())
            await expect(first_product).to_be_visible()

            # 4. Interact with the last matching element
            last_product = products.last
            print("Last product:", await last_product.inner_text())
            await expect(last_product).to_be_visible()

            # 5. Interact with a specific element using nth(index)
            third_product = products.nth(2)
            print("Third product:", await third_product.inner_text())
            await expect(third_product).to_be_visible()

            # 6. Loop through all matching elements and print their text
            for i in range(count):
                product_text = await products.nth(i).inner_text()
                print(f"Product {i + 1}: {product_text}")

            # 7. Verify the expected number of products
            assert count == 6
            await expect(products).to_have_count(6)

            print("All multiple locator checks passed!")

        finally:
            await browser.close()