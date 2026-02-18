
import allure

from pages.login_page import LoginPage

@allure.title("Valid Login Test")
@allure.description("Verify user can login with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
def test_valid_login(page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
