#Create a custom fixture that creates a new browser context.

import pytest

@pytest.fixture
def isolated_context(browser):
    context = browser.new_context()
    yield context
    context.close()


def test_isolated_context(isolated_context):
    page = isolated_context.new_page()
    page.goto("https://www.saucedemo.com/")
    assert "saucedemo.com" in page.url


