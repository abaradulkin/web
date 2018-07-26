from ui.main_page import *


__new_group_btn = s(by_css("#group-new>a"))
__import_group_btn = s(by_xpath("//li[@id='group-import']/a"))
__testtaker_list_save_btn = ss(by_xpath("//button[contains(text(), 'Save')]"))[1]

__testtaker_in_list_pattern = "//a[text()='{}']"
__group_pattern = "//li[@title='Group']//li[@title='{}']/a"


@step("Add testtaker to a group")
def add_testtaker_to_group(label):
    s(by_xpath(__testtaker_in_list_pattern.format(label))).click()
    __testtaker_list_save_btn.click()
    check_popup_message("Selection saved successfully")


@step("Create new group")
def create_new_group(label):
    __new_group_btn.click()
    wait_page_reloaded()
    set_name_and_save(label)
    check_popup_message("Group saved")


@step("Check testtaker in group list selected")
def is_testaker_selected(label):
    # Be careful, at start, when uncheck -> class=""
    # But if you check and uncheck again -> class="clicked uncheked"
    return "checked" in s(by_xpath(__testtaker_in_list_pattern.format(label))).get_attribute("class")
