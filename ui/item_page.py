from time import sleep
from selene import browser  # TODO: remove it letter
from selenium.webdriver.common.action_chains import ActionChains  # TODO: remove it letter
from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s

from ui import main_page


__work_area = s(by_css(".item-editor-drop-area"))
__save_btn = s(by_xpath("//li[@title='Save the item']"))
__choice_interaction_btn = s(by_css(".icon-choice"))

__response_btn = s(by_xpath("//span[@data-state='answer']"))
__choice_checkbox_pattern = "//li[@data-identifier='choice_{}']"

__widget_interaction = s(by_css(".widget-blockInteraction"))
__delete_interaction_btn = s(by_xpath("//span[@title='Choice Interaction']/following::div[@title='delete']"))



@step("Add choice to item")
def add_choice():
    # re-write this code using selene.elements
    __work_area.should(be.visible)
    s(by_css(".loading-bar")).should_not(be.visible)
    chain = ActionChains(browser.driver())
    chain.click_and_hold(__choice_interaction_btn).move_to_element(__work_area).perform()
    chain.release().perform()

@step("Select correct choice")
def select_correct_choice(num=1):
    __response_btn.click()
    s(by_xpath(__choice_checkbox_pattern.format(num))).click()


@step("Check that choice selected")
def check_choice_selected(num=1):
    s(by_xpath(__choice_checkbox_pattern.format(num))).should_have(have.css_class("user-selected"))


@step("Remove choice from item")
def remove_choice():
    __widget_interaction.click()
    __delete_interaction_btn.click()


@step("Save the item")
def save_item():
    __save_btn.click()
    main_page.check_popup_message("Your item has been saved")
