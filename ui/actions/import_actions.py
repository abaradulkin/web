from os.path import realpath, exists

from allure import step
from selene.bys import *
from selene.support.conditions import be, have
from selene.support.jquery_style_selectors import s


# Import options area
__content_package_radio_btn = by_id("importHandler_1")
__import_format_pattern = "//label[contains(text(), '{}')]"
__browse_file_btn = by_xpath("//input[@type='file']")
__file_type_label = by_id('file')
__file_success_status_icon = by_css(".status.success")
__import_button = by_css(".form-submitter")
__import_continue_btn = by_id("import-continue")
__status_message = by_css(".feedback-success")
__success_dialog_icon = by_css(".icon-success")


IMPORT_TYPES = {
    "rdf": "RDF",
    "zip": "QTI/APIP"
}

IMPORT_TYPES_MESSAGE = {
    "rdf": "Import Metadata from RDF file",
    "zip": "Import a QTI/APIP Content Package"
}


def make_import(file_path, import_message, import_type="rdf"):
    __select_import_type(import_type)
    __select_file_for_import(file_path, import_type)
    __accept_import(import_message)


@step("Select import type")
def __select_import_type(import_type):
    s(by_xpath(__import_format_pattern.format(IMPORT_TYPES[import_type]))).click()
    s(__file_type_label).should(have.text(IMPORT_TYPES_MESSAGE[import_type]))


@step("Select file to import and wait for verification")
def __select_file_for_import(file_path, extension):
    # TODO: change for relative path
    path = "./tao_tests/test_data/{}.{}".format(file_path, extension)
    print(realpath(path))
    s(__browse_file_btn).set_value(realpath(path))
    s(__file_success_status_icon).should_be(be.visible)


@step("Accept import and check import message")
def __accept_import(message):
    s(__import_button).click()
    s(__success_dialog_icon).should_be(be.visible, timeout=20)
    s(__status_message).should(have.text(message))
    s(__import_continue_btn).click()
