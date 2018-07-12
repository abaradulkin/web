from allure import step
from selene.bys import *
from selene.support.jquery_style_selectors import s


_login_field = by_name("login")
_password_field = by_name("password")
_log_in_button = by_name("connect")


@step("Make login with target account")
def make_login(login, password):
    s(_login_field).set_value(login)
    s(_password_field).set_value(password)
    s(_log_in_button).click()
