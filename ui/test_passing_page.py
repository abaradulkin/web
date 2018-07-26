from ui.main_page import *


__test_select_pattern = "//a/h3[text()='{}']"
__save_btn = by_id("saver")
__monitor_btn_pattern = "//h3[text()='{}']/following-sibling::div//span[contains(@class,'action play')]"
__play_btn_pattern = "//span[@title='{}']/parent::td/following-sibling::td[@class='actions authorizeCl']/button"
__delivery_status_pattern = "//span[@title='{}']/parent::td/following-sibling::td[@class='status']"
__popup_message = "//h3[text()='{}']/following-sibling::div"


def authorize_delivery(delivery_obj):
    s(by_xpath(__play_btn_pattern.format(delivery_obj.label))).click()
    ok_btn.click()
    check_popup_message("Sessions authorized")


def get_delivery_status(delivery_obj):
    return s(by_xpath(__delivery_status_pattern.format(delivery_obj.label))).text


def get_delivery_popup_message(delivery_obj):
    return s(by_xpath(__popup_message.format(delivery_obj.label))).text


def is_delivery_availiable(delivery_name):
    return s(by_xpath(__test_select_pattern.format(delivery_name.label))).is_displayed()


def select_delivery_for_passing(delivery_name):
    s(by_xpath(__test_select_pattern.format(delivery_name.label))).click()
    s(by_css(".loading-bar")).should_not(be.visible)


def choose_answer(index=None):
    if index:
        s(by_xpath("//input[@value='choice_{}']/following-sibling::span".format(index))).click()
    #s(by_xpath("//a/span[text()='Next']")).click()
    s(by_xpath("//li[@data-control='move-forward' or @data-control='move-end']/a")).click()


@step("Is test passion blocked")
def is_test_blocked():
    try:
        return s(by_xpath("//a[@class='block box']")).is_displayed()
    except TimeoutException:
        return False


@step("Open delivery monitor")
def open_delivery_monitor(delivery_obj):
    s(by_xpath(__monitor_btn_pattern.format(delivery_obj.label))).click()
    wait_page_reloaded()




def start_session(delivery_obj):
    s(by_xpath("//h3[text()='{}]//following::span[@class='action play']".format(delivery_obj.label)))
