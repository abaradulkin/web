from ui.main_page import *
from ui.actions import authoring_actions


__new_test_btn = s(by_xpath("//li[@id='test-new']/a"))
__import_test_btn = s(by_xpath("//li[@id='test-import']/a"))
__test_pattern = "//li[@title='Test']//li[@title='{}']/a"
__test_list = ss(by_xpath("//li[@title='Test']/ul/li"))


@step("Create new test")
def create_new_test(label):
    __new_test_btn.click()
    wait_page_reloaded()
    set_name_and_save(label)
    check_popup_message("Test saved")


@step("Import test from disk")
def import_test(test_name):
    __import_test_btn.click()
    import_actions.make_import(file_path=test_name, import_type="zip",
                               import_message="IMS QTI Test Package successfully imported.")
    wait_page_reloaded()


@step("Open target test")
def open_target_test(label):
    s(by_xpath(__test_pattern.format(label))).click()
    wait_page_reloaded()
    assert get_current_item_name() == label


@step("Open test authoring")
def open_test_authoring(label):
    open_target_test(label)
    open_authoring()



@step("Rename last test")
def rename_test(old_test_name, new_test_name):
    open_target_test(old_test_name)
    set_name_and_save(new_test_name)
    check_popup_message("Test saved")
