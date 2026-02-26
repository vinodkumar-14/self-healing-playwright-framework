
import allure


class TestLogin:

    @allure.id("Test_001")
    @allure.title("Test Login Scenarios")
    @allure.description("Verify whether user can login with invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_scenarios(self, config, login, user_data):
        username = user_data["username"]
        expected = user_data["expected"]

        login.navigate()
        start_time = login.login(username, config.password)

        if expected == "locked":
            login.validate_locked_user()
        else:
            login.validate_successful_login()

            if expected == "performance":
                login.validate_performance(start_time)

            if username == "error_user":
                login.validate_add_to_cart()

    @allure.id("Test_002")
    @allure.title("Test Login with invalid credentials")
    @allure.description("Verify whether user can login with invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login_with_invalid_credentials(self, config, login):
        login.navigate()
        login.login(config.username, "secret_sauc")
        login.validate_successful_login()

    @allure.id("Test_003")
    @allure.title("Test Login with empty credentials")
    @allure.description("Verify whether user can login with empty credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login_with_invalid_credentials(self, config, login):
        login.navigate()
        login.login("", "")
        login.validate_successful_login()
