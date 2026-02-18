
from pages.base_actions import BaseActions


class LoginPage:

    def __init__(self, page):
        self.page = page
        self.actions = BaseActions(page)

    def navigate(self):
        self.page.goto("https://www.saucedemo.com")
        self.page.wait_for_load_state("domcontentloaded")

    def login(self, username, password):
        # Intentionally wrong locator
        self.actions.enter_text("#username", username) # #user-name

        self.actions.enter_text("#password", password)

        # Intentionally wrong locator
        self.actions.click("#loginbutton")

        assert 'inventory' in self.page.url
