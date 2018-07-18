from time import sleep

from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s, ss
from ui.actions import import_actions

# Main and navigates elements for page
__username = s(by_css(".username"))
__popup_message = s(by_xpath("//div[@id='feedback-1']//div"))
__groups_btn = s(by_xpath("//a[@title='Group test takers according to global features and classifications.']"))
__delivery_btn = s(by_xpath("//a[@title='Prepare, publish deliveries sessions.']"))
__items_btn = s(by_xpath("//a[@title='Create and design items and exercises.']"))
__results_btn = s(by_xpath("//a[@title='View and format the collected results.']"))
__tests_btn = s(by_xpath("//a[@title='Combine a selection of items into tests.']"))
__test_takers_btn = s(by_xpath("//a[@title='Record and manage test-takers.']"))
__save_btn = s(by_name("Save"))

# Group actions and group list elements
__new_group_btn = s(by_css("#group-new>a"))
__import_group_btn = s(by_xpath("//li[@id='group-import']/a"))

__group_pattern = "//li[@title='Group']//li[@title='{}']/a"

# Delivery actions and delivery list elements
__new_delivery_btn = s(by("#delivery-new>a"))

# Item actions and item list elements
__new_item_btn = by_css("#item-new>a")
__delete_item_btn = by_xpath("//li[@id='item-delete']/a")
__import_item_btn = s(by_xpath("//li[@id='item-import']/a"))

__item_pattern = "//li[@title='Item']//li[@title='{}']/a"

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
__new_item_label_input = s(by_xpath("//label[text()='Label']/following-sibling::input"))
__authoring_btn = by_xpath("//li[@title='Authoring']/a")

# Diallog buttons
__delete_diallog_ok_btn = by_xpath("//button[@data-control='ok']")


def __wait_page_reloaded():
    #s(by_css(".loading-bar")).should(be.visible)
    sleep(1)
    s(by_css(".loading-bar")).should_not(be.visible)


@step("Add testtaker to a group")
def add_testtaker_to_group(testtaker_name):
    s(by_xpath("//a[text()='{}']".format(testtaker_name))).click()
    s(by_xpath("//footer//button[text()=' Save']")).click()
    check_popup_message("Selection saved successfully")


@step("Create new group")
def create_new_group(group_name):
    __new_group_btn.click()
    __wait_page_reloaded()
    set_name_and_save(group_name)
    check_popup_message("Group saved")


@step("Create new delivery")
def create_new_delivery(test_name, delivery_name=None, group_name=None):
    # Open delivery creation process
    __new_delivery_btn.click()
    __wait_page_reloaded()
    # Choose test for delivery
    __test_for_delivery_selection_field = s(by_id("select2-chosen-2"))
    __test_for_deliver_input = s(by_id("s2id_autogen2_search"))
    __test_for_delivery_element_pattern = "//div[text()='{}']"
    __publish_button = s(by_css(".action-label"))
    __test_for_delivery_selection_field.click()
    __test_for_deliver_input.set_value(test_name)
    s(by_xpath(__test_for_delivery_element_pattern.format(test_name))).click()
    __publish_button.click()
    check_popup_message("Publishing of \"{}\" completed".format(test_name))
    # Change delivery name
    if delivery_name:
        __new_item_label_input.set_value(delivery_name)
        ss(by_xpath("//button[text()='Save']"))[0].click()
        check_popup_message("Delivery saved")
    # Select groups for delivery
    if group_name:
        s(by_partial_link_text(group_name)).click()
        s(by_partial_link_text(group_name)).should(have.css_class("checked"))
        ss(by_xpath("//button[text()='Save']"))[1].click()
        check_popup_message("Selection saved successfully")


@step("Create new item")
def create_new_item(item_name):
    s(__new_item_btn).click()
    __wait_page_reloaded()
    set_name_and_save(item_name)
    check_popup_message("Item saved")


@step("Create new test")
def create_new_test(test_name):
    __new_test_btn.click()
    __wait_page_reloaded()
    set_name_and_save(test_name)
    check_popup_message("Test saved")


@step("Create new test taker")
def create_new_test_taker(test_taker):
    __new_test_taker_btn.click()
    __wait_page_reloaded()
    for key, value in test_taker.items():
        if key == "Interface Language":
            s(by_xpath(__testtaker_field_pattern.format(key, "select"))).click()
            s(by_xpath(__language_select_patter.format(value))).click()
        else:
            s(by_xpath(__testtaker_field_pattern.format(key, "input"))).set_value(value)
    __save_btn.click()
    check_popup_message("Test-taker saved")


@step("Check item exists in list")
def check_item_exists(item_name):
    s(by_xpath(__item_pattern.format(item_name))).is_displayed()


@step("Check popup with message")
def check_popup_message(message):
    __popup_message.should(have.text(message))
    __popup_message.should_not(be.visible)


@step("Check target user loggined")
def check_user_logged_in(username):
    __username.should(have.text(username))


@step("Delete target item")
def delete_target_item(item_name):
    open_target_item(item_name)
    s(__delete_item_btn).click()
    s(__delete_diallog_ok_btn).click()


@step("Get username for current user")
def get_active_user():
    return __username.text


@step("Import group from disk")
def import_group(group_name):
    __import_group_btn.click()
    import_actions.make_import(file_path=group_name, import_type="rdf",
                               import_message="Data imported successfully")
    __wait_page_reloaded()


@step("Import item from disk")
def import_item(item_name):
    __import_item_btn.click()
    import_actions.make_import(file_path=item_name, import_type="zip",
                               import_message="1 Item(s) of 1 imported from the given IMS QTI Package.")
    __wait_page_reloaded()


@step("Import testtaker from disk")
def import_testtaker(item_name):
    __import_testtaker_btn.click()
    import_actions.make_import(file_path=item_name, import_type="rdf",
                               import_message="Data imported successfully")
    __wait_page_reloaded()


@step("Import test from disk")
def import_test(test_name):
    __import_test_btn.click()
    import_actions.make_import(file_path=test_name, import_type="zip",
                               import_message="IMS QTI Test Package successfully imported.")
    __wait_page_reloaded()


@step("Make logout")
def logout():
    s(by_id("logout")).click()


@step("Open groups page")
def open_groups():
    __groups_btn.click()
    __wait_page_reloaded()


@step("Navigate to Deliveries tab")
def open_delivery():
    __delivery_btn.click()
    __wait_page_reloaded()


@step("Open items page")
def open_items():
    __items_btn.click()
    __wait_page_reloaded()


@step("Open item authoring")
def open_item_authoring(item_name):
    open_target_item(item_name)
    s(__authoring_btn).click()


@step("Open results page")
def open_results():
    __results_btn.click()
    __wait_page_reloaded()


@step("Open tests page")
def open_tests():
    __tests_btn.click()
    __wait_page_reloaded()


@step("Open test authoring")
def open_test_authoring(item_name):
    open_target_test(item_name)
    s(__authoring_btn).click()


@step("Open test taker page")
def open_test_takers():
    __test_takers_btn.click()
    __wait_page_reloaded()


@step("Open target group")
def open_target_group(group_name):
    s(by_xpath(__group_pattern.format(group_name))).click()
    __wait_page_reloaded()
    __new_item_label_input.should(have.value(group_name))

@step("Open target item")
def open_target_item(item_name):
    s(by_xpath(__item_pattern.format(item_name))).click()
    __wait_page_reloaded()
    __new_item_label_input.should(have.value(item_name))


@step("Open target test")
def open_target_test(test_name):
    s(by_xpath(__test_pattern.format(test_name))).click()
    __wait_page_reloaded()
    __new_item_label_input.should(have.value(test_name))


@step("Open target test taker")
def open_target_testtaker(testtaker_name):
    s(by_xpath(__testtaker_pattern.format(testtaker_name))).click()
    __wait_page_reloaded()


@step("Rename target group")
def rename_group(old_name, new_name):
    open_target_group(old_name)
    set_name_and_save(new_name)
    check_popup_message("Group saved")

@step("Rename target item")
def rename_item(old_item_name, new_item_name):
    open_target_item(old_item_name)
    set_name_and_save(new_item_name)
    check_popup_message("Item saved")


@step("Rename last test")
def rename_test(old_test_name, new_test_name):
    open_target_test(old_test_name)
    set_name_and_save(new_test_name)
    check_popup_message("Test saved")


@step("Rename test taker")
def rename_testtaker(old_name, new_name):
    open_target_testtaker(old_name)
    __wait_page_reloaded()
    s(by_xpath(__testtaker_field_pattern.format("Label", "input"))).set_value(new_name)
    __save_btn.click()
    check_popup_message("Test-taker saved")


@step("Set item name, save and check popup message")
def set_name_and_save(item_name):
    __new_item_label_input.set_value(item_name)
    __save_btn.click()
