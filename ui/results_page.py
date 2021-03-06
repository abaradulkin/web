from ui.main_page import *


__delivary_btn_pattern = "//li[@title='{}']/a"
__result_item_tattern = "//td[@class='ttaker' and text()='{}']/following-sibling::td//button[contains(@class,'view')]"
__label_text = element(by_xpath("//td[@class='field' and text()='Label:']/following-sibling::td[@class='fieldValue']"))
__login_text = element(by_xpath("//td[@class='field' and text()='Label:']/following-sibling::td[@class='fieldValue']"))

_score_list = elements(by_xpath("//td[text()='SCORE']/following-sibling::td[@class='dataResult']"))


def select_target_result(delivery_name, taker_name):
    element(by_xpath(__delivary_btn_pattern.format(delivery_name.label))).click()
    element(by_xpath(__result_item_tattern.format(taker_name.label))).click()


def get_item_score_by_index(index):
    return int(_score_list[index].text)


def get_testtaker_label():
    return __label_text.text


def get_testtaker_login():
    return __login_text.text