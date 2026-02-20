
import allure

from pages.base_actions import BaseActions
from config import config_reader

class LoginPage:

    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.actions = BaseActions(page)

    def navigate(self):
        self.page.goto(self.config.base_url)
        self.page.wait_for_load_state("domcontentloaded")

    def login(self, username=None, password=None):
        username = username or self.config.username
        password = password or self.config.password

        # Intentionally wrong locator
        self.actions.enter_text("#user-name", username) # Actual Locator: #user-name

        self.actions.enter_text("#password", password)

        # Intentionally wrong locator
        self.actions.click("#login-button") # Actual Locator: #login-button

        self.actions.validate_text(
            expected_locator=".app_logo",
            expected_text="Swag Labs",
            parent_locator=".login-box"
        )

        with allure.step('Login to saucedemo successfully.'):
            print('Login to saucedemo successfully.')
