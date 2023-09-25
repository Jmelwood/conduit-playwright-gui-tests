import pytest
from playwright.sync_api import Page, expect
from mimesis import Person
from mimesis.locales import Locale


# Create a separate set of random test data specific for the user creation test
@pytest.fixture(scope="module", autouse=True)
def new_user():
    person = Person(Locale.EN)
    username = person.username()
    email = person.email()
    password = person.password()
    return {"username": username, "email": email, "password": password}


def test_guest_can_login(page: Page, generic_user: dict[str, str]):
    page.goto("/#/")
    page.get_by_role("link", name="Sign in").click()
    page.get_by_placeholder("Email").click()
    page.get_by_placeholder("Email").fill(generic_user["email"])
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(generic_user["password"])
    page.get_by_role("button", name="Sign in").click()
    expect(page.get_by_role("link", name=generic_user["username"])).to_be_visible(
        timeout=10_000
    )


def test_guest_can_create_user(page: Page, new_user: dict[str, str]):
    page.goto("/#/")
    page.get_by_role("link", name="Sign up").click()
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill(new_user["username"])
    page.get_by_placeholder("Email").click()
    page.get_by_placeholder("Email").fill(new_user["email"])
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(new_user["password"])
    page.get_by_role("button", name="Sign up").click()
    expect(page.get_by_role("link", name=new_user["username"])).to_be_visible(
        timeout=10_000
    )


@pytest.mark.browser_context_args(storage_state="fixtures/generic_user.json")
def test_profile_page_has_correct_info(page: Page, generic_user: dict[str, str]):
    page.goto(f"/#/profile/{generic_user['username']}")
    expect(page.get_by_role("img")).to_have_attribute("src", generic_user["image"])
    expect(page.get_by_role("heading", name=generic_user["username"])).to_be_visible()
