from ui.main_page import *
from ui.actions import import_actions, authoring_actions

__item_pattern = "//li[@title='Item']//li[@title='{}']/a"
__new_item_btn = element(by_css("#item-new>a"))
__save_btn = element(by_xpath("//li[@title='Save the item']"))
__delete_item_btn = element(by_xpath("//li[(@id='item-delete' or @id='item-class-delete') and not(contains(@class, 'hidden'))]/a"))
__import_item_btn = element(by_xpath("//li[@id='item-import']/a"))
__interaction_div = element(by_xpath("//div[@data-qti-class='choiceInteraction']"))


@step("Check hac item an interaction")
def is_interaction_on_item():
    try:
        __interaction_div.should(be.visible, timeout=1)
        return True
    except TimeoutException:
        return False


@step("Import item from disk")
def import_item(item_name):
    __import_item_btn.click()
    import_actions.make_import(file_path=item_name, import_type="zip",
                               import_message="1 Item(s) of 1 imported from the given IMS QTI Package.")
    wait_page_reloaded()


@step("Click on deletion button and accept")
def make_deletion_action():
    __delete_item_btn.click()
    delete_diallog_ok_btn.click()


@step("Open target item")
def open_target_item(item_label):
    element(by_xpath(__item_pattern.format(item_label))).click()
    wait_page_reloaded()
    assert item_label == get_current_item_name()


@step("Start creation new Item")
def start_creation_new_item():
    __new_item_btn.click()
    wait_page_reloaded()
