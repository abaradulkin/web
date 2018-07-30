from ui.main_page import *


__lti_group_item = element(by_xpath("//li[@title='LTI Consumer']/a"))
__new_lti_btn = element("#lticonsumer-new>a")
__lti_label_input = element("#http_2_www_0_w3_0_org_1_2000_1_01_1_rdf-schema_3_label")
__lti_key_input = element("#http_2_www_0_tao_0_lu_1_Ontologies_1_TAO_0_rdf_3_OauthKey")
__lti_secret_input = element("#http_2_www_0_tao_0_lu_1_Ontologies_1_TAO_0_rdf_3_OauthSecret")


@step("Fill lti key")
def fill_lti_key(key):
    __lti_key_input.set_value(key)


@step("Fill lti label")
def fill_lti_label(label):
    __lti_label_input.set_value(label)


@step("Fill lti secret")
def fill_lti_secret(secret):
    __lti_secret_input.set_value(secret)

@step("Open LTI creation diallog")
def start_lti_creation():
    __lti_group_item.click()
    __new_lti_btn.click()
    #element("a>.icon-save").click()
