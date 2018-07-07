from selene.support.jquery_style_selectors import s
from selene.bys import *


_search_field = by_css(".searchbox-input")
_search_input = by_name("q")
_suggestion_total = by_css(".suggestion-total")

def get_suggection_total():
    return int(s(_suggestion_total).s(by_css(".suggestions-amount")).text)

def get_first_suggestion():
    return s(by_css(".suggestion")).s(by_css(".suggestion-name")).text

def enter_search_query(keyword):
    s(_search_field).click()
    s(_search_input).send_keys(keyword)

def make_search(keyword):
    enter_search_query(keyword)
    s(_search_input).submit()
