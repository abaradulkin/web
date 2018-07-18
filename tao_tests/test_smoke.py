from allure import feature, severity
from selene import browser, config
from selene.browsers import BrowserName

from framework.common.string_utilities import get_random_string
from ui import login_page, main_page, item_page, test_page, results_page
from utilities import factory


@feature("Smoke")
@severity("critical")
class TestSmoke(object):
    test_name = "admin"
    random_pattern = "auto_{}".format(get_random_string(4))

    def setup(self):
        config.browser_name = BrowserName.CHROME
        config.timeout = 7
        browser.open_url("http://spielplatz.taocloud.org/sprint81")
        login_page.make_login(self.test_name, self.test_name)

    @staticmethod
    def teardown():
        browser.close()

    def test_logging_in_as_administrator(self):
        main_page.check_user_logged_in(self.test_name)

    def test_items_creation(self):
        main_page.open_items()
        for i in range(4):
            item_name = "_".join([self.random_pattern, "item", str(i)])
            main_page.create_new_item(item_name)
            main_page.check_item_exists(item_name)

    def test_adding_interaction_to_item(self):
        for i in range(4):
            item_name = "_".join([self.random_pattern, "item", str(i)])
            main_page.open_items()
            main_page.open_item_authoring(item_name)
            item_page.add_choice()
            item_page.select_correct_choice(1)
            item_page.check_choice_selected(1)
            item_page.save_item()

    def test_remove_interaction_to_item(self):
        item_name = "_".join([self.random_pattern, "item", "3"])
        main_page.open_items()
        main_page.open_item_authoring(item_name)
        item_page.remove_choice()
        item_page.save_item()

    def test_item_deletion(self):
        item_name = "_".join([self.random_pattern, "item", "3"])
        main_page.open_items()
        main_page.delete_target_item(item_name)
        assert not main_page.check_item_exists(item_name)

    def test_test_creation(self):
        item_pattern = "_".join([self.random_pattern, "item", "{}"])
        test_name = "_".join([self.random_pattern, "test"])
        main_page.open_tests()
        main_page.create_new_test(test_name)
        main_page.open_test_authoring(test_name)
        for i in range(3):
            test_page.select_item(item_pattern.format(i))
        test_page.add_selected_items()
        test_page.save_test()

    def test_create_test_taker(self):
        main_page.open_test_takers()
        test_tacker = factory.create_testtacker(self.random_pattern)
        main_page.create_new_test_taker(test_tacker)

    def test_create_group(self):
        group_name = "_".join([self.random_pattern, "group"])
        taker_name = "_".join([self.random_pattern, "taker"])
        main_page.open_groups()
        main_page.create_new_group(group_name)
        main_page.add_testtaker_to_group(taker_name)

    def test_create_delivery(self):
        group_name = "_".join([self.random_pattern, "group"])
        test_name = "_".join([self.random_pattern, "test"])
        delivery_name = "_".join([self.random_pattern, "delivery"])
        main_page.open_delivery()
        main_page.create_new_delivery(test_name=test_name,
                                      group_name=group_name,
                                      delivery_name=delivery_name)

    def test_login_as_testtaker(self):
        taker_name = "_".join([self.random_pattern, "taker"])
        main_page.logout()
        login_page.make_login(taker_name, "change_me")

    def test_pass_test_as_testtaker(self):
        taker_name = "_".join([self.random_pattern, "taker"])
        delivery_name = "_".join([self.random_pattern, "delivery"])
        main_page.logout()
        login_page.make_login(taker_name, "change_me")
        test_page.select_delivery_for_passing(delivery_name)
        test_page.choose_answer()
        test_page.choose_answer(1)
        test_page.choose_answer(2)
        assert test_page.is_delivery_availiable(delivery_name)

    def test_view_results_as_administrator(self):
        taker_name = "_".join([self.random_pattern, "taker"])
        delivery_name = "_".join([self.random_pattern, "delivery"])
        main_page.open_results()
        results_page.select_target_result(delivery_name, taker_name)
        assert taker_name == results_page.get_testtaker_label()
        assert taker_name == results_page.get_testtaker_login()
        assert 0 == results_page.get_item_score_by_index(0)
        assert 1 == results_page.get_item_score_by_index(1)
        assert 0 == results_page.get_item_score_by_index(2)
