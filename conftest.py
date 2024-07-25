from pathlib import Path
import pytest
from playwright.sync_api import Playwright, expect
from mimesis import Person
from mimesis.locales import Locale

from pages.login_page import LoginPage

person = Person(Locale.EN)
username = person.username()
email = person.email()
password = person.password()


@pytest.fixture(scope="session", autouse=True)
def generic_user(playwright: Playwright):
    """
    Creates a generic user using the API directly.
    Returns the user's information given back by the API,
    including their profile picture URL and authentication token.
    Additionally saves the local storage token for ease of use.
    """

    api_request_context = playwright.request.new_context(
        base_url="https://api.realworld.io"
    )
    api_create_user = api_request_context.post(
        "/api/users",
        data={
            "user": {
                "username": username,
                "email": email,
                "password": password,
            }
        },
    )
    assert api_create_user.status == 201
    createdUser: dict = api_create_user.json()
    createdUser["user"]["password"] = password
    # Additionally, log in as the user and grab the local storage
    # to easily pre-authenticate for tests
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://react-ts-redux-realworld-example-app.netlify.app/#/login")
    LoginPage(page).login(createdUser["user"])
    expect(page.get_by_role("link", name=username)).to_be_visible(timeout=10_000)
    Path("fixtures").mkdir(parents=True, exist_ok=True)
    context.storage_state(path="fixtures/generic_user.json")
    browser.close()
    yield createdUser["user"]
