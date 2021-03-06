from ui.main_page import *
from ui.actions import import_actions



__delivery_pattern = "//li[@title='Assembled Delivery ']//li[@title='{}']/a"
__proctorin_option_checkbox = element("#http_2_www_0_tao_0_lu_1_Ontologies_1_TAODelivery_0_rdf_3_ProctorAccessible_0")
__new_delivery_btn = element(by("#delivery-new>a"))
__test_for_delivery_selection_field = element("#select2-chosen-2")
__test_for_deliver_input = element("#s2id_autogen2_search")
__test_for_delivery_element_pattern = "//div[text()='{}']"
__publish_button = element(".action-label")
__lti_btn = element("#lti-delivery-link")
__launch_url_input = element("#copyPasteBox")


@step("Get Launch URL to pass test via LTI")
def get_lti_link(label):
    open_target_delivery(label)
    __lti_btn.click()
    return __launch_url_input.text


@step("Open target delivery")
def open_target_delivery(delivery_obj):
    element(by_xpath(__delivery_pattern.format(delivery_obj.label))).click()
    wait_page_reloaded()
    assert delivery_obj.label == get_current_item_name()


@step("Select test for delivery")
def select_test_for_delivery(test_onj):
    __test_for_delivery_selection_field.click()
    __test_for_deliver_input.set_value(test_onj.label)
    element(by_xpath(__test_for_delivery_element_pattern.format(test_onj.label))).click()
    __publish_button.click()


@step("Select group for delivery")
def select_group_for_delivery(grooup_obj):
    element(by_partial_link_text(grooup_obj.label)).click()
    element(by_partial_link_text(grooup_obj.label)).should(have.css_class("checked"))
    elements(by_xpath("//button[text()='Save']"))[1].click()  # TODO: resolve problem witn save buttons


@step("Set proctoring option for delivery")
def set_proctoring(enabled=True):
    if __proctorin_option_checkbox.is_selected() != enabled:
        __proctorin_option_checkbox.click()
    assert __proctorin_option_checkbox.is_selected() == enabled, "Can't set up proctoring option for delivery"
    elements(by_xpath("//button[text()='Save']"))[0].click()  # TODO: move it to actions layer


@step("Start creation of new Delivery")
def start_creation_new_delivery():
    __new_delivery_btn.click()
    wait_page_reloaded()
