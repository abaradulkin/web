from time import sleep

from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s, ss


# Main and navigates elements for page
__username = by_css(".username")
__popup_message = s(by_xpath("//div[@id='feedback-1']//div"))
__groups_btn = s(by_xpath("//a[@title='Group test takers according to global features and classifications.']"))
__items_btn = s(by_xpath("//a[@title='Create and design items and exercises.']"))
__tests_btn = s(by_xpath("//a[@title='Combine a selection of items into tests.']"))
__test_takers_btn = s(by_xpath("//a[@title='Record and manage test-takers.']"))
__success_dialog_icon = by_css(".icon-success")
__save_btn = s(by_name("Save"))

# Group actions and group list elements
__new_group_btn = s(by_css("#group-new>a"))

# Item actions and item list elements
__new_item_btn = by_css("#item-new>a")
__delete_item_btn = by_xpath("//li[@id='item-delete']/a")
__import_item_btn = by_xpath("//li[@id='item-import']/a")

__item_pattern = "//li[@title='Item']//li[@title='{}']/a"

# Tests actions and tests list elements
__new_test_btn = s(by_xpath("//li[@id='test-new']/a"))
__test_pattern = "//li[@title='Test']//li[@title='{}']/a"

# Test-taker actions
__new_test_taker_btn = s(by_css("#testtaker-new>a"))
__testtaker_field_pattern = "//label[text()='{}']/following-sibling::{}"
__language_select_patter = "//option[text()='{}']"
__import_testtaker_btn = s(by_css("#testtaker-import>a"))

__testtaker_pattern = "//li[@title='Test-taker']//li[@title='{}']/a"

# Item editing area
__new_item_label_input = s(by_xpath("//label[text()='Label']/following-sibling::input"))
__authoring_btn = by_xpath("//li[@title='Authoring']/a")

# Import options area
__content_package_radio_btn = by_id("importHandler_1")
__browse_file_btn = by_xpath("//input[@type='file']")
__file_type_label = by_id('file')
__file_success_status_icon = by_css(".status.success")
__import_button = by_css(".form-submitter")
__import_continue_btn = by_id("import-continue")
__status_message = by_css(".feedback-success")

# Diallog buttons
__delete_diallog_ok_btn = by_xpath("//button[@data-control='ok']")


def __wait_page_reloaded():
    #s(by_css(".loading-bar")).should(be.visible)
    #s(by_css(".loading-bar")).should_not(be.visible)
    sleep(1)


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


@step("Delete target item")
def delete_target_item(item_name):
    open_target_item(item_name)
    s(__delete_item_btn).click()
    s(__delete_diallog_ok_btn).click()


@step("Get username for current user")
def get_active_user():
    return s(__username).text


# TODO: Move to import page
@step("Import item from disk")
def import_item(item_name):
    s(__import_item_btn).click()
    s(__content_package_radio_btn).click()
    s(__file_type_label).should(have.text("Import a QTI/APIP Content Package"))
    # TODO: change for relative path
    s(__browse_file_btn).set_value("/Users/alex/web/tao_tests/test_data/{}.zip".format(item_name))
    s(__file_success_status_icon).should_be(be.visible)
    s(__import_button).click()
    s(__success_dialog_icon).should_be(be.visible)
    s(__status_message).should(have.text("1 Item(s) of 1 imported from the given IMS QTI Package."))
    s(__import_continue_btn).click()
    __wait_page_reloaded()


# TODO: Move to import page
@step("Import testtaker from disk")
def import_testtaker(item_name):
    __import_testtaker_btn.click()
    s(__file_type_label).should(have.text("Import Metadata from RDF file"))
    # TODO: change for relative path
    s(__browse_file_btn).set_value("/Users/alex/web/tao_tests/test_data/{}.rdf".format(item_name))
    s(__file_success_status_icon).should_be(be.visible)
    s(__import_button).click()
    s(__success_dialog_icon).should_be(be.visible)
    s(__status_message).should(have.text("Data imported successfully"))
    s(__import_continue_btn).click()
    __wait_page_reloaded()


@step("Open groups page")
def open_groups():
    __groups_btn.click()
    __wait_page_reloaded()


@step("Open items page")
def open_items():
    __items_btn.click()
    __wait_page_reloaded()


@step("Open item authoring")
def open_item_authoring(item_name):
    open_target_item(item_name)
    s(__authoring_btn).click()


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


@step("Rename target item")
def rename_item(old_item_name, new_item_name):
    open_target_item(old_item_name)
    set_name_and_save(new_item_name)
    check_popup_message("Item saved")


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
