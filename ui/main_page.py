from time import sleep

from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s, ss
from selenium.common.exceptions import TimeoutException

# Main and navigates elements for page
__username = s(by_css(".username"))
__popup_message = s(by_xpath("//div[@id='feedback-1']//div"))
__groups_btn = s(by_xpath("//a[@title='Group test takers according to global features and classifications.']"))
__delivery_btn = s(by_xpath("//a[@title='Prepare, publish deliveries sessions.']"))
__items_btn = s(by_xpath("//a[@title='Create and design items and exercises.']"))
__results_btn = s(by_xpath("//a[@title='View and format the collected results.']"))
__tests_btn = s(by_xpath("//a[@title='Combine a selection of items into tests.']"))
__test_takers_btn = s(by_xpath("//a[@title='Record and manage test-takers.']"))
__language_select_patter = "//option[text()='{}']"
#__save_btn = s(by_name("Save"))
__save_btn = ss(by_xpath("//button[contains(text(), 'Save')]"))[0]
__create_btn = s("a>.icon-save")
__setting_btn = s("#settings")
__users_btn = s("#users")
__current_label_input = s(by_xpath("//label[text()='Label']/following-sibling::input"))
__logout_btn = s("#logout")
__home_btn = s("#home")

# Item editing area
__authoring_btn = by_xpath("//li[@title='Authoring']/a")

# Users page
__users_tab = s(by_xpath("//a[@href='#panel-add_user']"))


# Diallog buttons
delete_diallog_ok_btn = by_xpath("//button[@data-control='ok']")
ok_btn = s(by_xpath("//button[text()='OK']"))

# Settings page
__lti_tab = s(by_xpath("//a[@title='LTI Consumers']"))


# Basic operations wih general buttons, dialogs and sync
def wait_page_reloaded(timeout=10):
    #s(by_css(".loading-bar")).should(be.visible)
    sleep(1)
    s(by_css(".loading-bar")).should_not(be.visible, timeout=timeout)
    s(by_css(".loading")).should_not(be.visible, timeout=timeout)


@step("Check popup with message")
def check_popup_message(message, timeout=None):
    __popup_message.should(have.text(message), timeout=timeout)
    __popup_message.should_not(be.visible)


def get_current_item_name():
    return __current_label_input.get_attribute("value")


@step("Create")
def finish_creation_action():
    __create_btn.click()


@step("Save")
def save_current_object():
    __save_btn.click()


@step("Set item name and save")
def set_name_and_save(label, popup_msg=None):
    __current_label_input.set_value(label)
    save_current_object()
    if popup_msg:
        check_popup_message(popup_msg)


#################################
@step("Get current user name")
def get_loggined_username():
    return __username.text


@step("Get username for current user")
def get_active_user():
    return __username.text


@step("Return to home")
def home():
    __home_btn.click()


@step("Check user in users list")
def is_user_in_list(user, role=None):
    user_pattern = "//td[@class='login' and text()='{}']".format(user)
    if role:
        user_pattern = "{}/following-sibling::td[@class='roles' and text()='{}']".format(user_pattern, role)
    try:
        s(by_xpath(user_pattern)).should(be.visible)
        return True
    except TimeoutException:
        return False


@step("Check is item in list")
def is_object_in_list(item_name):
    try:
        return s(by_xpath("//li[@title='{}']/a".format(item_name))).is_displayed()
    except TimeoutException:
        return False


@step("Make logout")
def logout():
    __logout_btn.click()


@step("Open add user tab")
def open_add_user_tab():
    __users_tab.click()
    wait_page_reloaded()


@step("Open authoring")
def open_authoring():
    s(__authoring_btn).click()


@step("Open groups page")
def open_groups():
    __groups_btn.click()
    wait_page_reloaded()


@step("Navigate to Deliveries tab")
def open_delivery():
    __delivery_btn.click()
    wait_page_reloaded()


@step("Open items page")
def open_items():
    __items_btn.click()
    wait_page_reloaded()


@step("Open Settings > LTI tab")
def open_lti_tab():
    __lti_tab.click()


@step("Open results page")
def open_results():
    __results_btn.click()
    wait_page_reloaded()


@step("Open settings page")
def open_settings():
    __setting_btn.click()
    wait_page_reloaded()


@step("Open tests page")
def open_tests():
    __tests_btn.click()
    wait_page_reloaded()


@step("Open test taker page")
def open_test_takers():
    __test_takers_btn.click()
    wait_page_reloaded()


@step("Open users page")
def open_users():
    __users_btn.click()
    wait_page_reloaded()
