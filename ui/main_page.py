from time import sleep

from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s, ss
from selenium.common.exceptions import TimeoutException
from ui.actions import import_actions  # TODO: remove it later

# Main and navigates elements for page
__username = s(by_css(".username"))
__popup_message = s(by_xpath("//div[@id='feedback-1']//div"))
__groups_btn = s(by_xpath("//a[@title='Group test takers according to global features and classifications.']"))
__delivery_btn = s(by_xpath("//a[@title='Prepare, publish deliveries sessions.']"))
__items_btn = s(by_xpath("//a[@title='Create and design items and exercises.']"))
__results_btn = s(by_xpath("//a[@title='View and format the collected results.']"))
__tests_btn = s(by_xpath("//a[@title='Combine a selection of items into tests.']"))
__test_takers_btn = s(by_xpath("//a[@title='Record and manage test-takers.']"))
#__save_btn = s(by_name("Save"))
__save_btn = ss(by_xpath("//button[contains(text(), 'Save')]"))[0]
__create_btn = s("a>.icon-save")
__setting_btn = s("#settings")
__users_btn = s("#users")
__current_label_input = s(by_xpath("//label[text()='Label']/following-sibling::input"))
__logout_btn = s("#logout")
__home_btn = s("#home")

# Group actions and group list elements
__new_group_btn = s(by_css("#group-new>a"))
__import_group_btn = s(by_xpath("//li[@id='group-import']/a"))

__group_pattern = "//li[@title='Group']//li[@title='{}']/a"

# Tests actions and tests list elements
__new_test_btn = s(by_xpath("//li[@id='test-new']/a"))
__test_pattern = "//li[@title='Test']//li[@title='{}']/a"
__import_test_btn = s(by_xpath("//li[@id='test-import']/a"))
__test_list = ss(by_xpath("//li[@title='Test']/ul/li"))

# Test-taker actions
__new_test_taker_btn = s(by_css("#testtaker-new>a"))
__testtaker_field_pattern = "//label[text()='{}']/following-sibling::{}"
__language_select_patter = "//option[text()='{}']"
__import_testtaker_btn = s(by_css("#testtaker-import>a"))

__testtaker_pattern = "//li[@title='Test-taker']//li[@title='{}']/a"

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
def finish_Creation_Action():
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
@step("Add testtaker to a group")
def add_testtaker_to_group(testtaker_obj):
    s(by_xpath("//a[text()='{}']".format(testtaker_obj.label))).click()
    s(by_xpath("//footer//button[text()=' Save']")).click()
    check_popup_message("Selection saved successfully")


@step("Create new group")
def create_new_group(group_obj):
    __new_group_btn.click()
    wait_page_reloaded()
    set_name_and_save(group_obj.label)
    check_popup_message("Group saved")


@step("Create new test")
def create_new_test(test_obj):
    __new_test_btn.click()
    wait_page_reloaded()
    set_name_and_save(test_obj.label)
    check_popup_message("Test saved")


@step("Create new test taker")
def create_new_test_taker(testtaker_obj):
    __new_test_taker_btn.click()
    wait_page_reloaded()

    # TODO: make universal function
    s(by_xpath(__testtaker_field_pattern.format("Interface Language", "select"))).click()
    s(by_xpath(__language_select_patter.format(testtaker_obj.language))).click()
    s(by_xpath(__testtaker_field_pattern.format("Login", "input"))).set_value(testtaker_obj.login)
    s(by_xpath(__testtaker_field_pattern.format("Label", "input"))).set_value(testtaker_obj.label)
    s(by_xpath(__testtaker_field_pattern.format("Password", "input"))).set_value(testtaker_obj.password)
    s(by_xpath(__testtaker_field_pattern.format("Repeat password", "input"))).set_value(testtaker_obj.password)

    __save_btn.click()
    check_popup_message("Test-taker saved")


@step("Create new user")
def create_new_user(user_obj):
    __users_tab.click()
    wait_page_reloaded()

    s(by_xpath(__testtaker_field_pattern.format("Interface Language", "select"))).click()
    s(by_xpath(__language_select_patter.format(user_obj.language))).click()
    s(by_xpath(__testtaker_field_pattern.format("Login", "input"))).set_value(user_obj.login)
    s(by_xpath(__testtaker_field_pattern.format("Label", "input"))).set_value(user_obj.label)
    s(by_xpath(__testtaker_field_pattern.format("Password", "input"))).set_value(user_obj.password)
    s(by_xpath(__testtaker_field_pattern.format("Repeat password", "input"))).set_value(user_obj.password)
    s(by_xpath("//label[@class='elt_desc' and text()='{}']".format(user_obj.role))).click()

    __save_btn.click()
    check_popup_message("User added")


@step("Get current user name")
def get_loggined_username():
    return __username.text


@step("Get username for current user")
def get_active_user():
    return __username.text


@step("Return to home")
def home():
    __home_btn.click()


@step("Import group from disk")
def import_group(group_name):
    __import_group_btn.click()
    import_actions.make_import(file_path=group_name, import_type="rdf",
                               import_message="Data imported successfully")
    wait_page_reloaded()


@step("Import testtaker from disk")
def import_testtaker(item_name):
    __import_testtaker_btn.click()
    import_actions.make_import(file_path=item_name, import_type="rdf",
                               import_message="Data imported successfully")
    wait_page_reloaded()


@step("Import test from disk")
def import_test(test_name):
    __import_test_btn.click()
    import_actions.make_import(file_path=test_name, import_type="zip",
                               import_message="IMS QTI Test Package successfully imported.")
    wait_page_reloaded()


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
def is_item_in_list(item_name):
    try:
        return s(by_xpath("//li[@title='{}']/a".format(item_name))).is_displayed()
    except TimeoutException:
        return False


@step("Make logout")
def logout():
    __logout_btn.click()


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


@step("Open test authoring")
def open_test_authoring(item_obj):
    open_target_test(item_obj)
    s(__authoring_btn).click()


@step("Open test taker page")
def open_test_takers():
    __test_takers_btn.click()
    wait_page_reloaded()


@step("Open target group")
def open_target_group(group_name):
    s(by_xpath(__group_pattern.format(group_name))).click()
    wait_page_reloaded()
    __current_label_input.should(have.value(group_name))


@step("Open target test")
def open_target_test(test_obj):
    s(by_xpath(__test_pattern.format(test_obj.label))).click()
    wait_page_reloaded()
    __current_label_input.should(have.value(test_obj.label))


@step("Open target test taker")
def open_target_testtaker(testtaker_name):
    s(by_xpath(__testtaker_pattern.format(testtaker_name))).click()
    wait_page_reloaded()


@step("Open users page")
def open_users():
    __users_btn.click()
    wait_page_reloaded()


@step("Rename target group")
def rename_group(old_name, new_name):
    open_target_group(old_name)
    set_name_and_save(new_name)
    check_popup_message("Group saved")


@step("Rename last test")
def rename_test(old_test_name, new_test_name):
    open_target_test(old_test_name)
    set_name_and_save(new_test_name)
    check_popup_message("Test saved")


@step("Rename test taker")
def rename_testtaker(old_name, new_name):
    open_target_testtaker(old_name)
    wait_page_reloaded()
    s(by_xpath(__testtaker_field_pattern.format("Label", "input"))).set_value(new_name)
    __save_btn.click()
    check_popup_message("Test-taker saved")
