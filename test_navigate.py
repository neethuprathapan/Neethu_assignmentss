#Create a test that navigates to a website using the page fixture.

def test_open_website(page):
    page.goto("https://www.saucedemo.com/")

    assert page.url == "https://www.saucedemo.com/"


