import re
from playwright.sync_api import Page


class NavBarPage:
    def __init__(self, page: Page):
        self.page = page
        self.logo_button = page.locator("app-layout-header").get_by_role(
            "link", name="conduit"
        )
        self.home_link = page.get_by_role("link", name="Home")
        # Logged out options
        self.sign_in_link = page.get_by_role("link", name="Sign in")
        self.sign_up_link = page.get_by_role("link", name="Sign up")
        # Logged in options
        self.new_article_link = page.get_by_role("link", name=re.compile("New Article"))
        self.settings_link = page.get_by_role("link", name=re.compile("Settings"))
        self.profile_link = page.locator('a.nav-link[href*="profile"]')

    def goToFeedPage(self):
        self.home_link.click()

    def goToLoginPage(self):
        self.sign_in_link.click()

    def goToRegisterPage(self):
        self.sign_up_link.click()
