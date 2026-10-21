#Browser, Context and Page Fixtures

from playwright.sync_api import expect

def test_home_page(page):
    page.goto("https://www.saucedemo.com/")
    expect(page.get_by_text("Swag Labs")).to_be_visible()


def test_save_data(custom_page):
    custom_page.goto("https://www.saucedemo.com/")
    custom_page.evaluate("localStorage.setItem('data', 'neethu')")
    assert custom_page.evaluate("localStorage.getItem('data')") == "neethu"


def test_check_data(custom_page):
    custom_page.goto("https://www.saucedemo.com/")
    assert custom_page.evaluate("localStorage.getItem('data')") is None