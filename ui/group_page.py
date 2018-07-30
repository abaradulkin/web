from ui.main_page import *
from ui.actions import import_actions, authoring_actions

__new_group_btn = element(by_css("#group-new>a"))
__import_group_btn = element(by_xpath("//li[@id='group-import']/a"))
__testtaker_list_save_btn = elements(by_xpath("//button[contains(text(), 'Save')]"))[1]

__testtaker_in_list_pattern = "//a[text()='{}']"
__group_pattern = "//li[@title='Group']//li[@title='{}']/a"


@step("Add testtaker to a group")
def add_testtaker_to_group(label):
    element(by_xpath(__testtaker_in_list_pattern.format(label))).click()
    __testtaker_list_save_btn.click()
    check_popup_message("Selection saved successfully")


@step("Create new group")
def create_new_group(label):
    __new_group_btn.click()
    wait_page_reloaded()
    set_name_and_save(label)
    check_popup_message("Group saved")


@step("Import group from disk")
def import_group(group_name):
    __import_group_btn.click()
    import_actions.make_import(file_path=group_name, import_type="rdf",
                               import_message="Data imported successfully")
    wait_page_reloaded()


@step("Check testtaker in group list selected")
def is_testaker_selected(label):
    # Be careful, at start, when uncheck -> class=""
    # But if you check and uncheck again -> class="clicked uncheked"
    return "checked" in element(by_xpath(__testtaker_in_list_pattern.format(label))).get_attribute("class")


@step("Open target group")
def open_target_group(group_name):
    element(by_xpath(__group_pattern.format(group_name))).click()
    wait_page_reloaded()
    assert get_current_item_name() == group_name


@step("Rename target group")
def rename_group(old_name, new_name):
    open_target_group(old_name)
    set_name_and_save(new_name)
    check_popup_message("Group saved")
