from time import sleep
from selene import browser  # TODO: remove it letter
from selenium.webdriver.common.action_chains import ActionChains  # TODO: remove it letter
from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s
from selenium.common.exceptions import TimeoutException
from ui.main_page import *


__apply_btn = element("#installButton")
__plugin_checkbox_pattern = "#{}>td>.icon-checkbox-checked"
__plugin_pattern = "#{}>td>input"
__plugin_list_item_pattern = "//div[@id='extensions-manager-container']//following-sibling::td[text()='{}']"


@step("Check is plugin already installed")
def is_plugin_installed(plugin_name):
    try:
        element(__plugin_checkbox_pattern.format(plugin_name)).should(be.visible, timeout=1)
        #element(by_xpath(__plugin_list_item_pattern.format(plugin_name))).should(be.visible, timeout=1)
        return False
    except TimeoutException:
        return True


@step("Apply target setting")
def install_plugin(plugin_name):
    assert not is_plugin_installed(plugin_name), "Plugin {} already installed".format(plugin_name)
    element(__plugin_pattern.format(plugin_name)).click()
    __apply_btn.click()
    wait_page_reloaded()
    element(by_xpath("//button/span[text()='Yes']")).click()
    check_popup_message("Extension {} has been installed".format(plugin_name), timeout=30)
    wait_page_reloaded(60)
