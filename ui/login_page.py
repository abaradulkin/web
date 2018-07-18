from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s

from time import sleep

_login_field = s(by_name("login"))
_password_field = s(by_name("password"))
_log_in_button = s(by_name("connect"))


@step("Make login with target account")
def make_login(login, password):
    _login_field.set_value(login)
    _password_field.set_value(password)
    _log_in_button.click()
    #s(by_css(".loading-bar")).should(be.visible)
    sleep(1)
    s(by_css(".loading-bar")).should_not(be.visible)
