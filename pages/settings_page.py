import re
from playwright.sync_api import Page


class SettingsPage:
    def __init__(self, page: Page):
        self.page = page
        self.profile_pic_url_input = page.get_by_placeholder(re.compile("URL"))
        self.username_input = page.get_by_placeholder(re.compile("name"))
        self.bio_input = page.get_by_placeholder(re.compile("bio"))
        self.email_input = page.get_by_placeholder("Email")
        self.password_input = page.get_by_placeholder("Password")
        self.update_settings_button = page.get_by_role(
            "button", name=re.compile("settings")
        )
        self.logout_button = page.get_by_role("button", name=re.compile("logout"))
