#Pytest Configuration for Playwright

import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_home_page(page):
    page.goto("https://www.saucedemo.com/")
    expect(page.get_by_text("Swag Labs")).to_be_visible()


@pytest.mark.regression
def test_login_page_title(page):
    page.goto("https://www.saucedemo.com/")
    expect(page).to_have_title("Swag Labs")