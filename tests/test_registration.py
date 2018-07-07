import pytest

from selene.api import *
from selene import browser
from time import sleep

from ui import main_page, search_result_page
from selene import config
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager



class TestSearch(object):
    def setup(self):
        config.browser_name = "chrome"
        browser.open_url("https://mybook.ru")

    def teardown(self):
        browser.close()

    @pytest.mark.parametrize("keyword, results_num", [
        ("Google", 14),
        ("37 Geminorum", 1),
        ("dsljgnd", 0),
    ])
    def test_search_keyword(self, keyword, results_num):
        main_page.make_search(keyword)
        search_results = search_result_page.get_search_result()
        assert len(search_results) == results_num

    def test_search_suggestions_count(self):
        main_page.enter_search_query("Google")
        assert main_page.get_suggection_total() == 14

    def test_search_suggestion(selfs):
        main_page.enter_search_query("Google")
        assert "Google" in main_page.get_first_suggestion()

