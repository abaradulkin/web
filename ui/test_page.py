from selene import browser  # TODO: remove it letter
from selenium.webdriver.common.action_chains import ActionChains  # TODO: remove it letter
from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s

from ui import main_page


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
