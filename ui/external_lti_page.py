from allure import step
from selene import browser
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s, ss


@step("Open http://ltiapps.net/test/tc.php")
def open():
    browser.driver().get("http://ltiapps.net/test/tc.php")


@step("Set LTI key")
def fill_lti_key(key):
    s("#id_key").set_value(key)


@step("set LTI secret")
def fill_lti_secret(secret):
    s("#id_secret").set_value(secret)


@step("Set Launch URL")
def fill_launch_url(url):
    s(by_name("endpoint")).set_value(url)


@step("Set role")
def set_learner_role():
    s("#id_roles").clear()
    s("#id_a_role").click()
    s(by_xpath("//option[@value='Learner']")).click()


@step("Save launch options and start test")
def save_and_launch():
    s("#save_bottom").click()
    s("#launchw_bottom").click()
