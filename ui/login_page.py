from time import sleep

from allure import step
from selene.bys import *
from selene.support.conditions import be

from framework.ui.elements import element


_login_field = element(by_name("login"))
_password_field = element(by_name("password"))
_log_in_button = element(by_name("connect"))


@step("Make login with target account")
def make_login(login, password):
    _login_field.set_value(login)
    _password_field.set_value(password)
    _log_in_button.click()
    #element(by_css(".loading-bar")).should(be.visible)
    sleep(1)
    element(by_css(".loading-bar")).should_not(be.visible)
