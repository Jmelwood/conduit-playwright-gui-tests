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
    page.goto("/")
    yield


def test_guest_can_login(page: Page, generic_user: dict[str, str]):
    """
    Given I have a registered account\n
    When I navigate to the login page\n
    And I input/submit my credentials\n
    Then The main "feed" page loads successfully\n
    And The navigation bar changes to show my submitted username
    """
    NavBarPage(page).goToLoginPage()
    LoginPage(page).login(generic_user)
    expect(page.get_by_role("link", name=generic_user["username"])).to_be_visible(
        timeout=10_000
    )


def test_guest_can_create_user(page: Page, new_user: dict[str, str]):
    """
    Given I am a new user\n
    When I navigate to the register page\n
    And I input/submit new credentials\n
    Then The main "feed" page loads successfully\n
    And The navigation bar changes to show my submitted username
    """
    NavBarPage(page).goToRegisterPage()
    RegisterPage(page).register(new_user)
    expect(page.get_by_role("link", name=new_user["username"])).to_be_visible(
        timeout=10_000
    )


@pytest.mark.browser_context_args(storage_state="fixtures/generic_user.json")
def test_profile_page_has_correct_info(page: Page, generic_user: dict[str, str]):
    """
    Given I am logged into the application\n
    When I navigate to my profile page
    Then I see the correct (my) username and profile picture
    """
    page.goto(f"/#/profile/{generic_user['username']}")
    expect(page.locator("img.user-pic")).to_have_attribute("src", generic_user["image"])
    expect(NavBarPage(page).profile_link).to_have_text(generic_user["username"])
