import pytest
from playwright.sync_api import Page, expect
from mimesis import Person
from mimesis.locales import Locale

from pages.navbar_page import NavBarPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage


# Create a separate set of random test data specific for the user creation test
@pytest.fixture(scope="module", autouse=True)
def new_user():
    person = Person(Locale.EN)
    return {
        "username": person.username(),
        "email": person.email(),
        "password": person.password(),
    }


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.goto("/#/")
    yield


def test_guest_can_login(page: Page, generic_user: dict[str, str]):
    NavBarPage(page).goToLoginPage()
    LoginPage(page).login(generic_user)
    expect(page.get_by_role("link", name=generic_user["username"])).to_be_visible(
        timeout=10_000
    )


def test_guest_can_create_user(page: Page, new_user: dict[str, str]):
    NavBarPage(page).goToRegisterPage()
    RegisterPage(page).register(new_user)
    expect(page.get_by_role("link", name=new_user["username"])).to_be_visible(
        timeout=10_000
    )


@pytest.mark.browser_context_args(storage_state="fixtures/generic_user.json")
def test_profile_page_has_correct_info(page: Page, generic_user: dict[str, str]):
    page.goto(f"/#/profile/{generic_user['username']}")
    expect(page.get_by_role("img")).to_have_attribute("src", generic_user["image"])
    expect(page.get_by_role("heading", name=generic_user["username"])).to_be_visible()
