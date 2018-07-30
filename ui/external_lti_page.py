from allure import step
from selene import browser
from selene.bys import *

from framework.ui.elements import element


@step("Open http://ltiapps.net/test/tc.php")
def open():
    browser.driver().get("http://ltiapps.net/test/tc.php")


@step("Set LTI key")
def fill_lti_key(key):
    element("#id_key").set_value(key)


@step("set LTI secret")
def fill_lti_secret(secret):
    element("#id_secret").set_value(secret)


@step("Set Launch URL")
def fill_launch_url(url):
    element(by_name("endpoint")).set_value(url)


@step("Set role")
def set_learner_role():
    element("#id_roles").clear()
    element("#id_a_role").click()
    element(by_xpath("//option[@value='Learner']")).click()


@step("Save launch options and start test")
def save_and_launch():
    element("#save_bottom").click()
    element("#launchw_bottom").click()
