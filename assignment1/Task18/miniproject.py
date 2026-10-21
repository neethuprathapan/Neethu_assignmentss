#Integrated Mini Project

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from playwright.sync_api import expect, TimeoutError


def test_login_and_add_to_cart(setup_page, app_url):
    page = setup_page

    username = "standard_user"
    password = "secret_sauce"

    # assert username and password, "Set credentials in .env"

    # Open website
    page.goto(app_url)
    page.wait_for_timeout(5000)

    # Login
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()

    # Wait for inventory page
    page.wait_for_url("**/inventory.html")

    # Check products
    products = page.locator(".inventory_item_name")
    expect(products).to_have_count(6)

    # Use first, last and nth
    print("First:", products.first.inner_text())
    print("Last:", products.last.inner_text())
    print("Third:", products.nth(2).inner_text())

    # Add Backpack directly from the product listing
    backpack = page.locator(".inventory_item").filter(
        has_text="Sauce Labs Backpack"
    )
    backpack.get_by_role("button", name="Add to cart").click()

    # Wait for cart badge
    try:
        page.locator(".shopping_cart_badge").wait_for(
            state="visible",
            timeout=5000
        )
    except TimeoutError:
        raise AssertionError(
            "Cart badge did not appear after adding product."
        )

    # Verify cart count
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    # Open cart and verify product
    page.locator(".shopping_cart_link").click()
    expect(page.locator(".cart_item")).to_contain_text(
        "Sauce Labs Backpack"
    )

    print("Test passed!")


def test_browser_fixture(browser):
    assert browser.version
    print("Browser version:", browser.version)