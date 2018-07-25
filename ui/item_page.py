from selene import browser  # TODO: remove it letter
from selenium.webdriver.common.action_chains import ActionChains  # TODO: remove it letter

from ui.main_page import *
from ui.actions import import_actions

__choice_checkbox_pattern = "//li[@data-identifier='choice_{}']"
__choice_interaction_btn = s(by_css(".icon-choice"))
__delete_interaction_btn = s(by_xpath("//span[@title='Choice Interaction']/following::div[@title='delete']"))
__item_pattern = "//li[@title='Item']//li[@title='{}']/a"
__new_item_btn = by_css("#item-new>a")
__response_btn = s(by_xpath("//span[@data-state='answer']"))
__save_btn = s(by_xpath("//li[@title='Save the item']"))
__widget_interaction = s(by_css(".widget-blockInteraction"))
__work_area = s(by_css(".item-editor-drop-area"))
__delete_item_btn = by_xpath("//li[(@id='item-delete' or @id='item-class-delete') and not(contains(@class, 'hidden'))]/a")
__import_item_btn = s(by_xpath("//li[@id='item-import']/a"))
__interaction_div = s(by_xpath("//div[@data-qti-class='choiceInteraction']"))

@step("Add choice to item")
def add_choice():
    # re-write this code using selene.elements
    __work_area.should(be.visible)
    s(by_css(".loading-bar")).should_not(be.visible)
    chain = ActionChains(browser.driver())
    chain.click_and_hold(__choice_interaction_btn).move_to_element(__work_area).perform()
    chain.release().perform()


@step("Check that choice selected")
def check_choice_selected(num=1):
    s(by_xpath(__choice_checkbox_pattern.format(num))).should_have(have.css_class("user-selected"))


@step("Check hac item an interaction")
def is_interaction_on_item():
    try:
        return __interaction_div.is_displayed()
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
    s(__delete_item_btn).click()
    s(delete_diallog_ok_btn).click()


@step("Open item authoring")
def open_item_authoring(label):
    open_target_item(label)
    open_authoring()


@step("Save authoring")
def save_authoring():
    s("span>.icon-save").click()


@step("Open target item")
def open_target_item(item_label):
    s(by_xpath(__item_pattern.format(item_label))).click()
    wait_page_reloaded()
    assert item_label == get_current_item_name()


@step("Remove choice from item")
def remove_choice():
    __widget_interaction.click()
    __delete_interaction_btn.click()


@step("Select correct choice")
def select_correct_choice(num=1):
    __response_btn.click()
    s(by_xpath(__choice_checkbox_pattern.format(num))).click()


@step("Start creation new Item")
def start_creation_new_item():
    s(__new_item_btn).click()
    wait_page_reloaded()
