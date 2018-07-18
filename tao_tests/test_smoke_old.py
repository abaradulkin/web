import pytest
from allure import feature, severity
from selene import browser, config
from selene.browsers import BrowserName

from framework.common.string_utilities import get_random_string
from ui import login_page, main_page, item_page, test_page
from utilities import tao_api, factory


@feature("Smoke")
class TestSmoke(object):
    test_name = "admin"

    def setup(self):
        config.browser_name = BrowserName.CHROME
        config.timeout = 7
        browser.open_url("http://spielplatz.taocloud.org/sprint80")
        self.driver = browser.driver()

    @staticmethod
    def teardown():
        browser.close()

    @severity("critical")
    @pytest.mark.critical
    def test_logging_in_as_administrator(self):
        login_page.make_login(self.test_name, self.test_name)
        assert main_page.get_active_user() == self.test_name

    @severity("critical")
    @pytest.mark.slow
    def test_items_creation(self):
        login_page.make_login(self.test_name, self.test_name)
        item_pattern = "auto_{}_{}"
        random_key = get_random_string(4)
        for i in range(3):
            main_page.open_items()
            main_page.create_new_item(item_pattern.format(random_key, i))
            main_page.check_item_exists(item_pattern.format(random_key, i))

    @severity("critical")
    def test_item_deletion(self):
        item_name = "auto_{}".format(get_random_string(6))
        tao_api.create_item(item_name)
        login_page.make_login(self.test_name, self.test_name)
        main_page.open_items()
        main_page.delete_target_item(item_name)
        assert not main_page.check_item_exists(item_name)

    @severity("critical")
    def test_adding_interaction_to_item(self):
        item_name = "auto_{}".format(get_random_string(6))
        tao_api.create_item(item_name)
        login_page.make_login(self.test_name, self.test_name)
        main_page.open_items()
        main_page.open_item_authoring(item_name)
        item_page.add_choice()
        item_page.select_correct_choice(1)
        item_page.check_choice_selected(1)
        item_page.save_item()

    @severity("critical")
    @pytest.mark.slow
    def test_remove_interaction_to_item(self):
        default_import_item_name = "auto_item"
        item_name = "auto_{}".format(get_random_string(6))
        login_page.make_login(self.test_name, self.test_name)
        main_page.open_items()
        # TODO: realize import throw API
        main_page.import_item(default_import_item_name)
        main_page.rename_item(default_import_item_name, item_name)
        main_page.open_item_authoring(item_name)
        item_page.remove_choice()
        item_page.save_item()

    @severity("critical")
    def test_test_creation(self):
        test_pattern = "auto_{}".format(get_random_string(4)) + "_{}"
        test_name = test_pattern.format("test")
        for i in range(3):
            tao_api.create_item(test_pattern.format(i))
        login_page.make_login(self.test_name, self.test_name)
        main_page.open_tests()
        main_page.create_new_test(test_name)
        main_page.open_test_authoring(test_name)
        for i in range(3):
            test_page.select_item(test_pattern.format(i))
        test_page.add_selected_items()
        test_page.save_test()

    @severity("critical")
    def test_create_test_taker(self):
        login_page.make_login(self.test_name, self.test_name)
        main_page.open_test_takers()
        test_tacker = factory.create_testtacker()
        main_page.create_new_test_taker(test_tacker)

    @severity("critical")
    def test_create_group(self):
        test_pattern = "auto_{}" + "_{}".format(get_random_string(4))
        login_page.make_login(self.test_name, self.test_name)
        main_page.open_test_takers()
        main_page.import_testtaker("auto_testtaker")
        main_page.rename_testtaker("auto_testtaker", test_pattern.format("taker"))
        main_page.open_groups()
        main_page.create_new_group(test_pattern.format("group"))
        main_page.add_testtaker_to_group(test_pattern.format("taker"))

    @severity("critical")
    def test_create_delivery(self):
        test_pattern = "auto_{}" + "_{}".format(get_random_string(4))
        login_page.make_login(self.test_name, self.test_name)
        main_page.open_groups()
        main_page.import_group("auto_group")
        main_page.rename_group("auto_group", test_pattern.format("group"))
        main_page.open_tests()
        main_page.import_test("auto_test")
        main_page.rename_test("auto_test", test_pattern.format("test"))
        main_page.open_delivery()
        main_page.create_new_delivery(test_name=test_pattern.format("test"),
                                      group_name=test_pattern.format("group"),
                                      delivery_name=test_pattern.format("delivery"))
