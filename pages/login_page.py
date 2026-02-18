
import allure

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
        self.actions.enter_text("#username", username) # Actual Locator: #user-name

        self.actions.enter_text("#password", password)

        # Intentionally wrong locator
        self.actions.click("#loginbutton") # Actual Locator: #login-button

        assert 'inventory' in self.page.url

        header = self.page.locator("div.app_logo")
        header.wait_for(state="visible", timeout=5000)
        actual_text = header.inner_text().strip()
        expected_text = "Swag Labs"
        assert actual_text == expected_text, \
            f"Login failed. Expected '{expected_text}' but found '{actual_text}'"

        with allure.step('Login to saucedemo successfully.'):
            print('Login to saucedemo successfully.')
