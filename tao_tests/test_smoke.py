import pytest

from allure import feature, severity
from selene import browser, config
from selene.helpers import env

from ui import (login_page, main_page, item_page, test_passing_page, results_page, settings_page, delivery_page,
                group_page,
                test_creation_page, external_lti_page)
from step import admin_steps
from utilities.factory import TaoObjectFactory

CURRENT_SPRINT = "sprint81"


@pytest.fixture(scope='function')
def additional_tab():
    def switch(num=0):
        browser.driver().switch_to.window(browser.driver().window_handles[num])

    browser.driver().execute_script("window.open('');")
    switch(1)
    browser.open_url(CURRENT_SPRINT)
    switch(0)
    yield switch


@pytest.fixture(scope='session')
def tao_object_factory():
    factory = TaoObjectFactory()
    yield factory


@pytest.fixture(scope='session')
def four_items(tao_object_factory):
    items = [tao_object_factory.create_item() for i in range(4)]
    yield items


@pytest.fixture(scope='session')
def one_test(tao_object_factory):
    test = tao_object_factory.create_test()
    yield test


@pytest.fixture(scope='session')
def one_testtaker(tao_object_factory):
    testaker = tao_object_factory.create_user()
    yield testaker


@pytest.fixture(scope='session')
def one_group(tao_object_factory):
    group = tao_object_factory.create_group()
    yield group


@pytest.fixture(scope='session')
def one_delivery(tao_object_factory, one_test, one_group):
    delivery = tao_object_factory.create_delivery(one_test, one_group)
    yield delivery


@pytest.fixture(scope='session')
def one_proctor(tao_object_factory):
    proctor = tao_object_factory.create_user(role="Proctor")
    yield proctor


@pytest.fixture(scope='session')
def one_lti(tao_object_factory):
    lti = tao_object_factory.create_lti()
    yield lti


class BaseTest(object):
    config.browser_name = env("automation_platform", "chrome")
    config.timeout = 7
    admin_name = "admin"
    admin_pass = "admin"
    factory = TaoObjectFactory()

    def setup(self):
        browser.open_url(CURRENT_SPRINT)

    def teardown(self):
        browser.close()


@feature("Smoke")
@severity("critical")
class TestSmoke(BaseTest):
    """
    Suite with SmokeTest [https://onepoint.testrail.net/index.php?/suites/view/771]

    Tests:
    test_loggin_as_administrator - Logging in as Administrator [344164]
    test_create_items - Items creation [344165]
    test_add_interaction_to_item - Adding Interactions to Items [344167]
    test_remove_interaction_from_item - Deleting Interactions from Items [344168]
    test_delete_item - Items deletion [344166]
    test_create_test - Test creation [344169]
    test_create_testtaker - Test creation [344170]
    test_create_group - Group creation [344171]
    test_create_delivery - Delivery creation [344172]
    test_login_as_testtaker - Logging in as Test-taker [344173]
    test_pass_test_as_testtaker - Passing test as a Test-taker [344174]
    test_view_results_as_administrator - View results as Administrator [344175]
    test_install_proctoring - Install Proctoring [344176]
    test_create_proctor - Creating Proctor as Admin [344177]
    test_enable_proctoring_for_delivery - Enable proctoring for a delivery [344178]
    test_login_as_proctor - Logging as Proctor [344179]
    test_able_to_authorize_session - Able to authorize a session [344183] & Starting test [344184]
    test_create_lti - Create LTI Consumer as System Administrator [344180]
    test_launch_test_via_ltu - Launch a test via LTI [344181]
    """

    def test_loggin_as_administrator(self):
        login_page.make_login(self.admin_name, self.admin_pass)
        assert self.admin_name == main_page.get_loggined_username()

    def test_create_items(self, four_items):
        login_page.make_login(self.admin_name, self.admin_pass)
        for item in four_items:
            admin_steps.create_new_item(item)
            assert item_page.is_object_in_list(item.label)

    def test_add_interaction_to_item(self, four_items):
        login_page.make_login(self.admin_name, self.admin_pass)
        for item in four_items:
            admin_steps.add_interaction_to_item(item, choice=1)
            assert item_page.is_interaction_on_item()

    def test_remove_interaction_from_item(self, four_items):
        login_page.make_login(self.admin_name, self.admin_pass)
        # Last item used for remove interaction and delete them
        admin_steps.remove_interaction_from_item(four_items[-1])
        assert not item_page.is_interaction_on_item()

    def test_delete_item(self, four_items):
        login_page.make_login(self.admin_name, self.admin_pass)
        # Last item used for remove interaction and delete them
        admin_steps.delete_target_item(four_items[-1])
        assert not item_page.is_object_in_list(four_items[-1].label)

    def test_create_test(self, four_items, one_test):
        login_page.make_login(self.admin_name, self.admin_pass)
        # Last item deleted in test_delete_item
        admin_steps.create_new_test(one_test, four_items[:-1])
        main_page.open_tests()
        assert test_creation_page.is_object_in_list(one_test.label)

    def test_create_testtaker(self, one_testtaker):
        login_page.make_login(self.admin_name, self.admin_pass)
        admin_steps.create_new_testtaker(one_testtaker)
        assert main_page.is_object_in_list(one_testtaker.label)

    def test_create_group(self, one_group, one_testtaker):
        login_page.make_login(self.admin_name, self.admin_pass)
        main_page.open_groups()
        group_page.create_new_group(one_group.label)
        assert main_page.is_object_in_list(one_group.label)
        group_page.add_testtaker_to_group(one_testtaker.label)
        assert group_page.is_testaker_selected(one_testtaker.label)

    def test_create_delivery(self, one_delivery):
        login_page.make_login(self.admin_name, self.admin_pass)
        main_page.open_delivery()
        # TODO: realise delivery object as class, instead of namedtuple
        # self.suite_delivery.group = self.suite_group
        # self.suite_delivery.test = self.suite_test
        admin_steps.create_new_delivery(one_delivery)
        assert delivery_page.is_object_in_list(one_delivery.label)

    def test_login_as_testtaker(self, one_testtaker, one_delivery):
        login_page.make_login(one_testtaker.label, one_testtaker.password)
        assert test_passing_page.is_delivery_availiable(one_delivery)

    def test_pass_test_as_testtaker(self, one_testtaker, one_delivery):
        login_page.make_login(one_testtaker.label, one_testtaker.password)
        test_passing_page.select_delivery_for_passing(one_delivery)
        test_passing_page.choose_answer()
        test_passing_page.choose_answer(1)
        test_passing_page.choose_answer(2)
        assert test_passing_page.is_delivery_availiable(one_delivery)

    def test_view_results_as_administrator(self, one_testtaker, one_delivery):
        login_page.make_login(self.admin_name, self.admin_pass)
        main_page.open_results()
        results_page.select_target_result(one_delivery, one_testtaker)
        assert one_testtaker.label == results_page.get_testtaker_label()
        assert one_testtaker.login == results_page.get_testtaker_login()
        assert 0 == results_page.get_item_score_by_index(0)
        assert 1 == results_page.get_item_score_by_index(1)
        assert 0 == results_page.get_item_score_by_index(2)

    @feature("Proctoring")
    def test_install_proctoring(self):
        login_page.make_login(self.admin_name, self.admin_pass)
        main_page.open_settings()
        plugin_name = "taoProctoring"
        if settings_page.is_plugin_installed(plugin_name):
            pytest.skip("{} plugin already installed".format(plugin_name))
        settings_page.install_plugin(plugin_name)
        main_page.open_settings()
        assert settings_page.is_plugin_installed(plugin_name)

    @feature("Proctoring")
    def test_create_proctor(self, one_proctor):
        login_page.make_login(self.admin_name, self.admin_pass)
        main_page.open_users()
        admin_steps.create_new_user(one_proctor)
        assert main_page.is_user_in_list(one_proctor.login, one_proctor.role)

    @feature("Proctoring")
    def test_enable_proctoring_for_delivery(self, one_delivery):
        login_page.make_login(self.admin_name, self.admin_pass)
        main_page.open_delivery()
        delivery_page.open_target_delivery(one_delivery)
        delivery_page.set_proctoring(enabled=True)
        delivery_page.check_popup_message("Delivery saved")  # instead of assert

    @feature("Proctoring")
    def test_login_as_proctor(self, one_proctor, one_delivery):
        login_page.make_login(one_proctor.label, one_proctor.password)
        assert test_passing_page.is_delivery_availiable(one_delivery)

    @feature("Proctoring")
    def test_able_to_authorize_session(self, additional_tab, one_proctor, one_testtaker, one_delivery):
        # Try to start test as TestTaker
        login_page.make_login(one_testtaker.label, one_testtaker.password)
        test_passing_page.select_delivery_for_passing(one_delivery)
        assert test_passing_page.get_delivery_popup_message(
            one_delivery) == "Please wait, authorization in process ..."
        # Authorize test as Proctor
        additional_tab(1)
        login_page.make_login(one_proctor.label, one_proctor.password)
        test_passing_page.open_delivery_monitor(one_delivery)
        test_passing_page.authorize_delivery(one_delivery)
        assert test_passing_page.get_delivery_status(one_delivery) == "Authorized but not started"
        # Check that test authorized
        additional_tab(0)
        browser.driver().refresh()
        login_page.make_login(one_testtaker.label, one_testtaker.password)
        assert test_passing_page.get_delivery_popup_message(one_delivery) == "Authorized, you may proceed"

    @feature("LTI")
    def test_create_lti(self, one_lti):
        login_page.make_login(self.admin_name, self.admin_pass)
        admin_steps.create_new_lti(one_lti)
        assert main_page.is_object_in_list(one_lti.label)

    @feature("LTI")
    def test_launch_test_via_lti(self, additional_tab, one_delivery, one_lti):
        login_page.make_login(self.admin_name, self.admin_pass)
        main_page.open_delivery()
        lti_link = delivery_page.get_lti_link(one_delivery)
        external_lti_page.open()
        external_lti_page.fill_launch_url(lti_link)
        external_lti_page.fill_lti_key(one_lti.key)
        external_lti_page.fill_lti_secret(one_lti.secret)
        external_lti_page.set_learner_role()
        external_lti_page.save_and_launch()
        additional_tab(2)
        assert test_passing_page.is_delivery_availiable(one_delivery)
