from ui.main_page import *
from ui.actions import import_actions


__import_testtaker_btn = s(by_css("#testtaker-import>a"))
__new_test_taker_btn = s(by_css("#testtaker-new>a"))

__language_select_patter = "//option[text()='{}']"
__testtaker_field_pattern = "//label[text()='{}']/following-sibling::{}"
__testtaker_pattern = "//li[@title='Test-taker']//li[@title='{}']/a"


@step("Fill testtaker label")
def fill_label(label):
    s(by_xpath(__testtaker_field_pattern.format("Label", "input"))).set_value(label)


@step("Select language for testaker")
def select_language(language):
    s(by_xpath(__testtaker_field_pattern.format("Interface Language", "select"))).click()
    s(by_xpath(__language_select_patter.format(language))).click()


@step("Fill testtaker login")
def fill_login(login):
    s(by_xpath(__testtaker_field_pattern.format("Login", "input"))).set_value(login)


@step("Fill testtaker password")
def fill_password(password):
    s(by_xpath(__testtaker_field_pattern.format("Password", "input"))).set_value(password)
    s(by_xpath(__testtaker_field_pattern.format("Repeat password", "input"))).set_value(password)


@step("Fill user role")
def fill_role(role):
    s(by_xpath("//label[@class='elt_desc' and text()='{}']".format(role))).click()


@step("Import testtaker from disk")
def import_testtaker(item_name):
    __import_testtaker_btn.click()
    import_actions.make_import(file_path=item_name, import_type="rdf",
                               import_message="Data imported successfully")
    wait_page_reloaded()


@step("Open target test taker")
def open_target_testtaker(testtaker_name):
    s(by_xpath(__testtaker_pattern.format(testtaker_name))).click()
    wait_page_reloaded()


@step("Rename test taker")
def rename_testtaker(old_name, new_name):
    open_target_testtaker(old_name)
    wait_page_reloaded()
    s(by_xpath(__testtaker_field_pattern.format("Label", "input"))).set_value(new_name)
    save_current_object()
    check_popup_message("Test-taker saved")


@step("Start new testtaker creation")
def start_testtaker_creation():
    __new_test_taker_btn.click()
    wait_page_reloaded()
