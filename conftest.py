import allure
from selene import browser


# TODO: find possibility to understand, is browser launched
def pytest_exception_interact(node, call, report):
    if False:
        allure.attach.file(source=browser.take_screenshot(), name='Screenshot')
