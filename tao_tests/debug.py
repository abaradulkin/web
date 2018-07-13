from selene import browser
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selene.support.jquery_style_selectors import s
from selene.support.conditions import be, have
from selene.bys import *


driver = webdriver.Remote(
        command_executor='http://127.0.0.1:63729',
        desired_capabilities={})
old_session = driver.session_id
driver.close()
driver.session_id = "fff32c83896f1f7e6df712e3adb930cd"
browser.set_driver(driver)

sleep(1)
btn = by_xpath("//li[@data-identifier='{}']".format("choice_1"))
print("user-selected" in s(btn).get_attribute('class'))
s(btn).should_have(have.css_class("user-selected"))

btn = by_xpath("//li[@data-identifier='{}']".format("choice_2"))
print("user-selected" in s(btn).get_attribute('class'))
