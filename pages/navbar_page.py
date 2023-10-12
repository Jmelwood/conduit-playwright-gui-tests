from playwright.sync_api import Page


class NavBarPage:
    def __init__(self, page: Page):
        self.page = page
        self.logo_button = page.get_by_role("navigation").get_by_role(
            "link", name="conduit"
        )
        self.home_link = page.get_by_role("link", name="Home")
        self.sign_in_link = page.get_by_role("link", name="Sign in")
        self.sign_up_link = page.get_by_role("link", name="Sign up")

    def goToFeedPage(self):
        self.home_link.click()

    def goToLoginPage(self):
        self.sign_in_link.click()

    def goToRegisterPage(self):
        self.sign_up_link.click()
