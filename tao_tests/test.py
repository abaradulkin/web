import pytest
from time import sleep

from allure import feature, severity
from selene import browser
from selene.browsers import BrowserName
from selene import config

from ui import login_page, main_page

from framework.common.string_utilities import get_random_string
from tao_tests import tao_api

@feature("Smoke")
class TestSmoke(object):
    test_name = "admin"

    def setup(self):
        config.browser_name = BrowserName.CHROME
        browser.open_url("http://spielplatz.taocloud.org/sprint80")

    def teardown(self):
        browser.close()

    @severity("critical")
    def test_logging_in_as_administrator(self):
        login_page.make_login(self.test_name, self.test_name)
        assert main_page.get_active_user() == self.test_name

    @severity("critical")
    def test_items_creation(self):
        login_page.make_login(self.test_name, self.test_name)
        item_pattern = "auto_{}_{}"
        random_key = get_random_string(4)
        for i in range(3):
            main_page.open_items()
            main_page.create_new_item(item_pattern.format(random_key, i))
            assert main_page.check_item_exists(item_pattern.format(random_key, i))

    def test_item_deletion(self):
        item_name = "auto_{}".format(get_random_string(6))
        assert tao_api.create_item(item_name)
        login_page.make_login(self.test_name, self.test_name)
        main_page.open_items()
        main_page.delete_target_item(item_name)
        assert not main_page.check_item_exists(item_name)
