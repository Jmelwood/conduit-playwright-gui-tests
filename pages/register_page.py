from playwright.sync_api import Page


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.sign_up_header = page.get_by_role("heading", name="Sign up")
        self.have_account_link = page.get_by_role("link", name="Have an account?")
        self.username_input = page.get_by_placeholder("Username")
        self.email_input = page.get_by_placeholder("Email")
        self.password_input = page.get_by_placeholder("Password")
        self.sign_up_button = page.get_by_role("button", name="Sign up")

    def register(self, user: dict[str, str]):
        self.username_input.fill(user["username"])
        self.email_input.fill(user["email"])
        self.password_input.fill(user["password"])
        self.sign_up_button.click()
