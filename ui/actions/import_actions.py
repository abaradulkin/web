from os.path import realpath

from allure import step
from selene.bys import *
from selene.support.conditions import be, have

from framework.ui.elements import element


# Import options area
__browse_file_btn = element(by_xpath("//input[@type='file']"))
__content_package_radio_btn = element("#importHandler_1")
__file_success_status_icon = element(".status.success")
__file_type_label = element('#file')
__import_button = element(".form-submitter")
__import_continue_btn = element("#import-continue")
__status_message = element(".feedback-success")
__success_dialog_icon = element(".icon-success")

__import_format_pattern = "//label[contains(text(), '{}')]"


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
    element(by_xpath(__import_format_pattern.format(IMPORT_TYPES[import_type]))).click()
    __file_type_label.should(have.text(IMPORT_TYPES_MESSAGE[import_type]))


@step("Select file to import and wait for verification")
def __select_file_for_import(file_path, extension):
    # TODO: change for relative path
    path = "./tao_tests/test_data/{}.{}".format(file_path, extension)
    __browse_file_btn.set_value(realpath(path))
    __file_success_status_icon.should_be(be.visible)


@step("Accept import and check import message")
def __accept_import(message):
    __import_button.click()
    __success_dialog_icon.should_be(be.visible, timeout=20)
    __status_message.should(have.text(message))
    __import_continue_btn.click()
