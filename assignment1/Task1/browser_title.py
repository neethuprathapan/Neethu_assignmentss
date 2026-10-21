import pytest
from playwright.sync_api import sync_playwright, expect


def test_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://demowebshop.tricentis.com/")
        print("Page title:", page.title())
        expect(page).to_have_title("Demo Web Shop")