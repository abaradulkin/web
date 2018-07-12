from time import sleep

from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s


# Main and navigates elements for page
__username = by_css(".username")
__popup_message = by_id("feedback-1")
__items_btn = by_xpath("//a[@title='Create and design items and exercises.']")
__success_dialog_icon = by_css(".icon-success")

# Item actions and item list elements
__new_item_btn = by_xpath("//li[@id='item-new']/a")
__delete_item_btn = by_xpath("//li[@id='item-delete']/a")
__import_item_btn = by_xpath("//li[@id='item-import']/a")

__item_pattern = "//li[@title='Item']//li[@title='{}']/a"

# Item editing area
__new_item_label_input = by_xpath("//label[text()='Label']/following-sibling::input")
__new_item_save_btn = by_name("Save")
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


@step("Create new item")
def create_new_item(item_name):
    s(__new_item_btn).click()
    __wait_page_reloaded()
    set_name_and_save(item_name)


@step("Check item exists in list")
def check_item_exists(item_name):
    s(by_xpath(__item_pattern.format(item_name))).is_displayed()


@step("Check popup with message")
def check_popup_message(message):
    s(__popup_message).should(have.text(message))
    s(__popup_message).should_not(be.visible)


@step("Delete target item")
def delete_target_item(item_name):
    open_target_item(item_name)
    s(__delete_item_btn).click()
    s(__delete_diallog_ok_btn).click()


@step("Get username for current user")
def get_active_user():
    return s(__username).text


@step("Import item from disk")
def import_item(item_name):
    s(__import_item_btn).click()
    s(__content_package_radio_btn).click()
    s(__file_type_label).should(have.text("Import a QTI/APIP Content Package"))
    s(__browse_file_btn).set_value("/Users/alex/web/{}.zip".format(item_name))
    s(__file_success_status_icon).should_be(be.visible)
    s(__import_button).click()
    s(__success_dialog_icon).should_be(be.visible)
    s(__status_message).should(have.text("1 Item(s) of 1 imported from the given IMS QTI Package."))
    s(__import_continue_btn).click()
    __wait_page_reloaded()


@step("Open items page")
def open_items():
    s(__items_btn).click()
    __wait_page_reloaded()


@step("Open target item")
def open_target_item(item_name):
    s(by_xpath(__item_pattern.format(item_name))).click()
    __wait_page_reloaded()
    s(__new_item_label_input).should(have.value(item_name))


@step("Open item authoring")
def open_item_authoring(item_name):
    open_target_item(item_name)
    s(__authoring_btn).click()


@step("Rename target item")
def rename_item(old_item_name, new_item_name):
    open_target_item(old_item_name)
    set_name_and_save(new_item_name)


@step("Set item name, save and check popup message")
def set_name_and_save(item_name):
    s(__new_item_label_input).set_value(item_name)
    s(__new_item_save_btn).click()
    check_popup_message("Item saved")
