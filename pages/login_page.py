
from pages.base_actions import BaseActions


class LoginPage:

    def __init__(self, page):
        self.page = page
        self.actions = BaseActions(page)

    def navigate(self):
        self.page.goto("https://www.saucedemo.com")
        self.page.wait_for_load_state("domcontentloaded")

    def login(self, username, password):
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)

        # Intentionally wrong locator
        self.actions.click("#loginbutton")
