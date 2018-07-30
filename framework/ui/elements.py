import selene.driver

from selene.elements import *
from selene.support.conditions import be


class SeleneElementModified(SeleneElement):
    def highlight(self):
        def action(it):
            def apply_style(s):
                it._parent.execute_script("arguments[0].setAttribute('style', arguments[1]);", it, s)

            original_style = it.get_attribute('style')
            apply_style("background: yellow; border: 2px solid red;")
            from time import sleep
            sleep(0.3)
            apply_style(original_style)
        self._execute_on_webelement(
            action,
            condition=be.visible)
        return self  # todo: think on: IWebElement#click was supposed to return None

    def click(self):
        def action(it):
            def apply_style(s):
                it._parent.execute_script("arguments[0].setAttribute('style', arguments[1]);", it, s)

            original_style = it.get_attribute('style')
            apply_style("background: yellow; border: 2px solid red;")
            from time import sleep
            sleep(0.3)
            apply_style(original_style)
            it.click()
        self._execute_on_webelement(
            action,
            condition=be.visible)
        return self  # todo: think on: IWebElement#click was supposed to return None

    @classmethod
    def by_css_or_by(cls, css_selector_or_by, webdriver, context=None):
        if not context:
            context = webdriver

        return SeleneElementModified.by(
            css_or_by_to_by(css_selector_or_by),
            webdriver,
            context)

    @classmethod
    def by(cls, by, webdriver, context=None):
        # type: (Tuple[str, str], IWebDriver, ISearchContext) -> SeleneElement
        if not context:
            context = webdriver

        return SeleneElementModified(WebDriverWebElementLocator(by, context), webdriver)


class SeleneCollectionModified(SeleneCollection):
    def element_by(self, condition):
        return SeleneElementModified(FoundByConditionWebElementLocator(condition, self), self._webdriver)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SeleneCollection(
                SlicedListWebElementLocator(index, collection=self),
                self._webdriver)
        return SeleneElementModified(IndexedWebElementLocator(index, collection=self), self._webdriver)


def element(css_selector_or_by):
    return SeleneElementModified.by_css_or_by(css_selector_or_by, selene.driver._shared_driver)


def elements(css_selector_or_by):
    return SeleneCollectionModified.by_css_or_by(css_selector_or_by, selene.driver._shared_driver)
