
import allure


class TestInventory:

    @allure.id("Test_004")
    @allure.title("Test inventory checkout without user information")
    @allure.description("Verify whether user can checkout without user information")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_without_user_information(self, config, login, inventory):
        login.navigate()
        login.login(config.username, config.password)
        inventory.checkout_complete(
            "Sauce Labs Backpack",
            "Vinodkumar",
            "Kouthal",
            "560102"
        )
