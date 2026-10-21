# Secrets Management & Secure Credentials

import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect


# Load the local .env file from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def test_saucedemo_login():
    username = os.getenv("SAUCE_USERNAME")
    password = os.getenv("SAUCE_PASSWORD")

    # Verify credentials exist without printing them
    assert username, "SAUCE_USERNAME is missing"
    assert password, "SAUCE_PASSWORD is missing"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=1000)

        try:
            page = browser.new_page()
            page.goto("https://www.saucedemo.com/")

            page.locator("#user-name").fill(username)
            page.locator("#password").fill(password)
            page.locator("#login-button").click()

            expect(page.locator(".inventory_list")).to_be_visible()

        finally:
            browser.close()