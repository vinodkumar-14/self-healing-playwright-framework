
import allure

from pages.base_actions import BaseActions

class Inventory:

    def __init__(self, page):
        self.page = page
        self.actions = BaseActions(page)

    @allure.step("Add inventory item and checkout: {inventory_name}")
    def add_inventory_and_checkout(self, inventory_name: str):
        """
        Clicks 'Add to cart' button for given inventory name and click 'cart' button
        :param inventory_name: Exact product name as displayed
        """
        # click on 'add to cart'
        item = self.page.locator(".inventory_item", has_text=inventory_name)
        item.locator("button", has_text="Add to cart").click()

        # click on cart button
        self.actions.click("[data-test='shopping-cart-link']")

        # click on checkout
        self.actions.click("#checkout")

    @allure.step("Checkout: Your information: {first_name} {last_name} {zip_or_postal_code}")
    def checkout_your_information(self, first_name, last_name, zip_or_postal_code):
        """
        Provide first name, last name & zip_or_postal_code and click on checkout button
        :param first_name: First name
        :param last_name: Last name
        :param zip_or_postal_code: Zip/Postal code
        """
        self.actions.enter_text("#first-name", first_name)
        # self.actions.enter_text("#last-name", last_name)
        # self.actions.enter_text("#postal-code", zip_or_postal_code)
        self.actions.click("#continue")

        self.actions.validate_text(
            expected_locator=".title",
            expected_text="Checkout: Overview",
            parent_locator=".error"
        )

    @allure.step("Checkout: Overview")
    def checkout_overview(self):
        """
        Click on 'finish' button to complete place the order
        """
        self.actions.click("#finish")

        self.actions.validate_text(
            expected_locator="[data-test='complete-header']",
            expected_text="Thank you for your order!"
        )

    @allure.step("Add inventory item and checkout complete: {inventory_name} {first_name} "
                 "{last_name} {zip_or_postal_code}")
    def checkout_complete(self, inventory_name, first_name, last_name, zip_or_postal_code):
        """
        Choose the inventory item
            - Click on 'Add to cart' button
            - Click 'cart' button
            - Click 'checkout' button
            - Fill the User information and click on checkout button
            - Click on 'Finish' button to place the order
        :param inventory_name: Inventory name
        :param first_name: First name
        :param last_name: Last name
        :param zip_or_postal_code: zip/postal code
        """
        self.add_inventory_and_checkout(inventory_name)
        self.checkout_your_information(first_name, last_name, zip_or_postal_code)
        self.checkout_overview()

        with allure.step('Order placed successfully.'):
            print('Order placed successfully.')
