
from framework.pages.base_actions import BaseActions

from playwright.sync_api import expect

import allure
import time


class LoginPage:

    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.actions = BaseActions(page, config)

        # locators
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")
        self.inventory_list = page.locator(".inventory_list")
        self.cart_badge = page.locator(".shopping_cart_badge")

    @allure.step('Navigate to the URL')
    def navigate(self):
        self.page.goto(self.config.base_url)
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Login into to saucedemo")
    def login(self, username=None, password=None):
        username = self.config.username if username is None else username
        password = self.config.password if password is None else password

        # Intentionally wrong locator
        self.actions.enter_text("#user-name", username) # Actual Locator: #user-name
        self.actions.enter_text("#password", password)

        start_time = time.time()

        # Intentionally wrong locator
        self.actions.click("#login-button") # Actual Locator: #login-button

        # self.actions.validate_text(
        #     expected_locator=".app_logo",
        #     expected_text="Swag Labs",
        #     parent_locator=".login-box"
        # )
        #
        # with allure.step('Login to saucedemo successfully.'):
        #     print('Login to saucedemo successfully.')

        return start_time

    @allure.step('Validate the locked out user')
    def validate_locked_user(self):
        self.actions.validate_text(
            expected_locator=self.error_message,
            expected_text="Epic sadface: Sorry, this user has been locked out."
        )

        with allure.step('Locked out user Found.'):
            print('Locked out user Found.')

    @allure.step('Login successfully login user')
    def validate_successful_login(self):
        self.actions.validate_text(
            expected_locator=".app_logo",
            expected_text="Swag Labs",
            parent_locator=".login-box"
        )

        with allure.step('Login to saucedemo successfully.'):
            print('Login to saucedemo successfully.')

    @staticmethod
    @allure.step('Validate performance after login')
    def validate_performance(start_time, threshold=10):
        load_time = time.time() - start_time
        assert load_time < threshold, f"Login took {load_time} seconds"

        with allure.step("Login performance is within threshold."
                         f"Load Time: {load_time} seconds."
                         f"Threshold: {threshold} seconds."):
            print("Login performance is within threshold."
                         f"Load Time: {load_time} seconds."
                         f"Threshold: {threshold} seconds.")

    @allure.step('Validate Add to Cart after login')
    def validate_add_to_cart(self):
        self.page.locator("text=Add to cart").first.click()
        expect(self.cart_badge).to_be_visible()
