import pytest
from config import BASE_URL
from playwright.sync_api import expect


def test_home_page(configured_page):
    configured_page.goto(BASE_URL)
    expect(configured_page.get_by_text("Swag Labs")).to_be_visible()