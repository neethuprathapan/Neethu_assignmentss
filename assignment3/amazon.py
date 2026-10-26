
import os
import pytest
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


@pytest.mark.smoke
def test_amazon_shopping_journey():
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        context = browser.new_context(
            viewport={"width": 1366, "height": 900}
        )
        page = context.new_page()

        try:
            # 1. Open Amazon India and verify the landing page
            page.goto(
                "https://www.amazon.in/",
                wait_until="domcontentloaded",
                timeout=60000
            )
            page.locator("#twotabsearchtextbox").wait_for(
                state="visible", timeout=30000
            )

            assert "amazon.in" in page.url
            print("PASS: Amazon India landing page loaded")

            # 2. Hover over the account/sign-in menu
            account_menu = page.locator("#nav-link-accountList")
            account_menu.hover()

            dropdown = page.locator("#nav-al-container")

            try:
                dropdown.wait_for(state="visible", timeout=5000)
                print("PASS: Account hover menu is visible")
            except PlaywrightTimeoutError:
                print("INFO: Account dropdown was unavailable")

            # 9. Check hidden menu state and reveal it normally
            # Do not force-click hidden elements.
            if dropdown.count() > 0:
                if not dropdown.is_visible():
                    print("PASS: Account dropdown is initially hidden")
                    account_menu.hover()
                    try:
                        dropdown.wait_for(
                            state="visible", timeout=5000
                        )
                        print("PASS: Hover revealed the dropdown")
                    except PlaywrightTimeoutError:
                        print("INFO: Dropdown did not become visible")
                else:
                    print(
                        "INFO: Dropdown was already visible; "
                        "initial hidden state not verified"
                    )

            # 3. Enter a query and wait for dynamic suggestions
            search_box = page.locator("#twotabsearchtextbox")
            search_box.fill("python programming book")

            suggestions = page.locator(
                ".s-suggestion:visible"
            )

            selected_suggestion = False

            try:
                suggestions.first.wait_for(
                    state="visible", timeout=7000
                )

                # Select a suggestion by its visible text
                matching = suggestions.filter(
                    has_text="python"
                )

                if matching.count() > 0:
                    print(
                        "Suggestion selected:",
                        matching.first.inner_text()
                    )
                    matching.first.click()
                else:
                    print(
                        "Selecting first visible suggestion:",
                        suggestions.first.inner_text()
                    )
                    suggestions.first.click()

                selected_suggestion = True

            except PlaywrightTimeoutError:
                print(
                    "INFO: No visible autocomplete suggestion; "
                    "submitting the search query instead"
                )

            if not selected_suggestion:
                search_box.press("Enter")

            page.wait_for_load_state(
                "domcontentloaded", timeout=30000
            )

            # 4. Search for a non-restricted product
            # If a suggestion was selected, perform a unique search
            # explicitly so the product results are predictable.
            search_box = page.locator("#twotabsearchtextbox")
            search_box.wait_for(state="visible", timeout=20000)
            search_box.fill("Python Crash Course book")
            search_box.press("Enter")

            page.wait_for_load_state(
                "domcontentloaded", timeout=30000
            )

            results = page.locator(
                '[data-component-type="s-search-result"]'
            )
            results.first.wait_for(
                state="visible", timeout=30000
            )

            print("PASS: Search results are displayed")

            # 5. Scroll down incrementally and inspect content
            previous_height = page.evaluate(
                "() => document.body.scrollHeight"
            )

            for step in range(1, 5):
                page.evaluate(
                    "() => window.scrollBy(0, 600)"
                )
                page.wait_for_timeout(700)

                visible_results = results.count()
                current_height = page.evaluate(
                    "() => document.body.scrollHeight"
                )

                print(
                    f"Scroll {step}: "
                    f"results={visible_results}, "
                    f"page height={current_height}"
                )

            if current_height > previous_height:
                print("PASS: Additional page height detected")
            else:
                print(
                    "INFO: Page height did not increase; "
                    "checking pagination or existing results"
                )

            pagination = page.locator(
                ".s-pagination-next"
            )

            if pagination.count() > 0:
                print(
                    "Pagination control present:",
                    pagination.first.get_attribute("aria-label")
                )
            else:
                print(
                    "INFO: No standard next-page control detected"
                )

            # Return to the results near the top
            page.evaluate("() => window.scrollTo(0, 0)")

            # 6. Open the first product with a visible title link
            page.evaluate("() => window.scrollTo(0, 0)")

            product_link = page.locator(
                '[data-component-type="s-search-result"] h2 a:visible'
            ).first

            try:
                product_link.wait_for(state="visible", timeout=15000)

                print("Product link found:", product_link.inner_text())
                product_link.click()

                page.wait_for_load_state(
                    "domcontentloaded", timeout=30000
                )

            except PlaywrightTimeoutError:
                page.screenshot(
                    path="screenshots/amazon_search_debug.png",
                    full_page=True
                )
                raise AssertionError(
                    "No visible product title link found. "
                    "Check screenshots/amazon_search_debug.png "
                    "to see what Amazon displayed."
                )

            # Verify the product details page
            title = page.locator("#productTitle")
            title.wait_for(state="visible", timeout=30000)

            product_title = title.inner_text().strip()
            assert product_title, "Product title is empty"

            print("PASS: Product details page opened:", product_title)

            page.wait_for_load_state(
                "domcontentloaded", timeout=30000
            )

            title = page.locator("#productTitle")
            title.wait_for(state="visible", timeout=30000)

            product_title = title.inner_text().strip()
            assert product_title, "Product title is empty"
            print("PASS: Product title:", product_title)

            # Look for a displayed price
            price = page.locator(
                "#corePriceDisplay_desktop_feature_div "
                ".a-price .a-offscreen"
            ).first

            if price.count() == 0:
                price = page.locator(
                    "#priceblock_ourprice, "
                    "#priceblock_dealprice, "
                    "#price_inside_buybox, "
                    ".apexPriceToPay .a-offscreen, "
                    "#corePrice_feature_div .a-price "
                    ".a-offscreen"
                ).first

            if price.count() > 0 and price.is_visible():
                print(
                    "PASS: Product price:",
                    price.inner_text().strip()
                )
            else:
                print(
                    "INFO: A visible price was not found. "
                    "The product may have a different price layout "
                    "or no current offer."
                )

            # 7. Right-click a harmless element
            # Playwright can dispatch the right-click, but native
            # browser context menus are not reliably inspectable.
            title.click(button="right")
            print("PASS: Right-click interaction performed")

            # 8. Double-click a harmless text label
            title.dblclick()
            print("PASS: Double-click interaction performed")

            # 10. Capture final product details evidence
            page.evaluate("() => window.scrollTo(0, 0)")
            page.wait_for_timeout(1000)

            screenshot_path = os.path.join(
                screenshot_dir,
                "amazon_product_details.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            print("PASS: Final screenshot saved:", screenshot_path)
            print("PASS: Shopping journey completed without purchase")

        finally:
            browser.close()
