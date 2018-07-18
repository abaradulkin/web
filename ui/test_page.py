from selene import browser  # TODO: remove it letter
from selenium.webdriver.common.action_chains import ActionChains  # TODO: remove it letter
from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s

from ui import main_page


__test_select_pattern = "//a/h3[text()='{}']"


def is_delivery_availiable(delivery_name):
    return s(by_xpath(__test_select_pattern.format(delivery_name))).is_displayed()


def select_delivery_for_passing(delivery_name):
    s(by_xpath(__test_select_pattern.format(delivery_name))).click()
    s(by_css(".loading-bar")).should_not(be.visible)


def choose_answer(index=None):
    if index:
        s(by_xpath("//input[@value='choice_{}']/following-sibling::span".format(index))).click()
    #s(by_xpath("//a/span[text()='Next']")).click()
    s(by_xpath("//li[@data-control='move-forward' or @data-control='move-end']/a")).click()


# TODO: move it to another page
#__item_select_patern = "//li[@class='instance']//a[@title='{}']"
#__add_selection_btn = s(by_xpath("//ol[@data-msg='Add selected item(s) here.']/div"))
__add_selection_btn = s(by_css(".itemref-placeholder"))
__save_btn = by_id("saver")

@step("Select item to include in test")
def select_item(item_name):
    s(by_link_text(item_name)).click()


@step("Add selected items to test")
def add_selected_items():
    __add_selection_btn.click()


@step("Save the test")
def save_test():
    s(__save_btn).click()
    main_page.check_popup_message("Test Saved")
