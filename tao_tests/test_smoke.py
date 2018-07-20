import pytest

from allure import feature, severity
from selene import browser, config
from selene.helpers import env

from ui import login_page, main_page, item_page, test_page, results_page, settings_page
from utilities.factory import TaoObjectFactory


class BaseTest(object):
    config.browser_name = env("automation_platform", "chrome")
    config.timeout = 7
    admin_name = "admin"
    factory = TaoObjectFactory()

    def setup(self):
        browser.open_url("sprint80")

    def teardown(self):
        browser.close()


@feature("Smoke")
@severity("critical")
class TestSmoke(BaseTest):
    suite_items = [BaseTest.factory.create_item() for i in range(4)]  # 3 for creation check and 1 for deletion
    suite_test = BaseTest.factory.create_item()
    suite_testtaker = BaseTest.factory.create_user()
    suite_group = BaseTest.factory.create_group()
    suite_delivery = BaseTest.factory.create_delivery(suite_test, suite_group)

    def setup(self):
        super().setup()
        login_page.make_login(self.admin_name, self.admin_name)

    def test_logging_in_as_administrator(self):
        main_page.check_user_logged_in(self.admin_name)

    def test_items_creation(self):
        main_page.open_items()
        for item in self.suite_items:
            main_page.create_new_item(item)
            main_page.check_item_exists(item)

    def test_adding_interaction_to_item(self):
        for item in self.suite_items:
            main_page.open_items()
            main_page.open_item_authoring(item)
            item_page.add_choice()
            item_page.select_correct_choice(1)
            item_page.check_choice_selected(1)
            item_page.save_item()

    def test_remove_interaction_to_item(self):
        main_page.open_items()
        main_page.open_item_authoring(self.suite_items[-1])
        item_page.remove_choice()
        item_page.save_item()

    def test_item_deletion(self):
        main_page.open_items()
        main_page.delete_target_item(self.suite_items[-1])
        assert not main_page.check_item_exists(self.suite_items[-1])

    def test_test_creation(self):
        main_page.open_tests()
        main_page.create_new_test(self.suite_test)
        main_page.open_test_authoring(self.suite_test)
        for item in self.suite_items[:-1]:
            test_page.select_item(item)
        test_page.add_selected_items()
        test_page.save_test()

    def test_create_test_taker(self):
        main_page.open_test_takers()
        main_page.create_new_test_taker(self.suite_testtaker)

    def test_create_group(self):
        main_page.open_groups()
        main_page.create_new_group(self.suite_group)
        main_page.add_testtaker_to_group(self.suite_testtaker)

    def test_create_delivery(self):
        main_page.open_delivery()
        # TODO: realise delivery object as class, instead of namedtouple
        # self.suite_delivery.group = self.suite_group
        # self.suite_delivery.test = self.suite_test
        main_page.create_new_delivery(self.suite_delivery)

    def test_login_as_testtaker(self):
        main_page.logout()
        login_page.make_login(self.suite_testtaker.label, self.suite_testtaker.password)
        test_page.is_delivery_availiable(self.suite_delivery)

    def test_pass_test_as_testtaker(self):
        main_page.logout()
        login_page.make_login(self.suite_testtaker.label, self.suite_testtaker.password)
        test_page.select_delivery_for_passing(self.suite_delivery)
        test_page.choose_answer()
        test_page.choose_answer(1)
        test_page.choose_answer(2)
        assert test_page.is_delivery_availiable(self.suite_delivery)

    def test_view_results_as_administrator(self):
        main_page.open_results()
        results_page.select_target_result(self.suite_delivery, self.suite_testtaker)
        assert self.suite_testtaker.label == results_page.get_testtaker_label()
        assert self.suite_testtaker.login == results_page.get_testtaker_login()
        assert 0 == results_page.get_item_score_by_index(0)
        assert 1 == results_page.get_item_score_by_index(1)
        assert 0 == results_page.get_item_score_by_index(2)


@feature("Smoke")
@severity("critical")
class TestProctorSmoke(BaseTest):
    def setup(self):
        super().setup()
        login_page.make_login(self.admin_name, self.admin_name)

    def test_install_proctoring(self):
        main_page.open_settings()
        plugin_name = "taoProctoring"
        if settings_page.is_plugin_installed(plugin_name):
            pytest.skip("{} plugin already installed".format(plugin_name))
        settings_page.install_plugin(plugin_name)
        main_page.open_settings()
        assert settings_page.is_plugin_installed(plugin_name)

    def test_create_proctor(self):
        suite_proctor = self.factory.create_user(role="Proctor")
        main_page.open_users()
        main_page.create_new_user(suite_proctor)
        assert main_page.is_user_in_list(suite_proctor.login, suite_proctor.role)