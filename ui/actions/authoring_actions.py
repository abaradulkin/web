from allure import step
from selene import browser  # TODO: remove it letter
from selenium.webdriver.common.action_chains import ActionChains  # TODO: remove it letter
from selene.bys import *
from selene.support.conditions import be, have

from framework.ui.elements import element


__add_selection_btn = element(by_css(".itemref-placeholder"))
__save_btn = element("#saver")
__work_area = element(by_css(".item-editor-drop-area"))
__choice_interaction_btn = element(by_css(".icon-choice"))
__delete_interaction_btn = element(by_xpath("//span[@title='Choice Interaction']/following::div[@title='delete']"))
__widget_interaction = element(by_css(".widget-blockInteraction"))
__response_btn = element(by_xpath("//span[@data-state='answer']"))

__choice_checkbox_pattern = "//li[@data-identifier='choice_{}']"


@step("Add choice to item")
def add_choice():
    # re-write this code using selene.elements
    __work_area.should(be.visible)
    element(by_css(".loading-bar")).should_not(be.visible)
    chain = ActionChains(browser.driver())
    chain.click_and_hold(__choice_interaction_btn).move_to_element(__work_area).perform()
    chain.release().perform()


@step("Add selected items to test")
def add_selected_items():
    __add_selection_btn.click()


@step("Check that choice selected")
def check_choice_selected(num=1):
    element(by_xpath(__choice_checkbox_pattern.format(num))).should_have(have.css_class("user-selected"))


@step("Save autoring")
def save():
    __save_btn.click()


def save_items():
    element(by_xpath("//span[contains(text(), 'Save')]")).click()


@step("Select item to include in test")
def select_item(item_obj):
    element(by_link_text(item_obj.label)).click()


@step("Select correct choice")
def select_correct_choice(num=1):
    __response_btn.click()
    element(by_xpath(__choice_checkbox_pattern.format(num))).click()

@step("Remove choice from item")
def remove_choice():
    __widget_interaction.click()
    __delete_interaction_btn.click()
