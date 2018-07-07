# encoding=utf-8
from selene.support.jquery_style_selectors import s, ss
from selene.bys import *

result_item = by_css(".search-result__item")
#"//div[@class='search-result__item search-result__item_book first_child']"

def get_search_result():
    return ss(result_item)