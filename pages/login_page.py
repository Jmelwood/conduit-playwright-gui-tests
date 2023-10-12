from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.sign_in_header = page.get_by_role("heading", name="Sign in")
        self.need_account_link = page.get_by_role("link", name="Need an account?")
        self.email_input = page.get_by_placeholder("Email")
        self.password_input = page.get_by_placeholder("Password")
        self.sign_in_button = page.get_by_role("button", name="Sign in")

    def login(self, user: dict[str, str]):
        self.email_input.fill(user["email"])
        self.password_input.fill(user["password"])
        self.sign_in_button.click()
