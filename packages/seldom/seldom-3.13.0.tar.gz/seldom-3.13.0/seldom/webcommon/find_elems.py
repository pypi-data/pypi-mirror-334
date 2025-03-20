import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from seldom.logging.exceptions import NotFindElementError
from seldom.running.config import Seldom
from seldom.webcommon.locators import LOCATOR_LIST
from seldom.webcommon.selector import selection_checker


class WebElement:
    """Web Element API"""

    def __init__(self, browser, selector: str = None, **kwargs) -> None:
        self.browser = browser
        if selector is not None:
            self.by, self.value = selection_checker(selector)
        else:
            if not kwargs:
                raise ValueError("Please specify a locator.")
            if len(kwargs) > 1:
                raise ValueError("Please specify only one locator.")

            by, self.value = next(iter(kwargs.items()))
            self.by = LOCATOR_LIST.get(by)
            if not self.by:
                raise ValueError(f"The find element locator is not supported: {by}. ")

        self.find_elem_info = None
        self.find_elem_warn = None

    def find(self, index: int = None, empty: bool = False, highlight: bool = False):
        """
        Return the element(s) found by the locator.
        :param index:
        :param empty:
        :param highlight:
        :return:
        """
        # Use WebDriverWait instead of time.sleep for smarter waiting
        try:
            elems = WebDriverWait(self.browser, Seldom.timeout).until(
                EC.presence_of_all_elements_located((self.by, self.value))
            )
            self.find_elem_info = f"Found {len(elems)} element(s): {self.by}={self.value}"
        except TimeoutException:
            self.find_elem_warn = f"❌ No elements found for: {self.by}={self.value}"
            if not empty:
                raise NotFindElementError(self.find_elem_warn)
            return []

        if index is None:
            return elems

        # Return specific element by index
        if index < len(elems):
            # element highlight
            if highlight is True:
                self._highlight_element(elems[index])

            return elems[index]

        raise IndexError(f"Index {index} out of bounds for the found elements.")

    def _highlight_element(self, elem=None) -> None:
        """
        Highlight the element on the page for debugging purposes.
        :param elem: Web element to be highlighted
        """
        if Seldom.app_server is not None and Seldom.app_info is not None:
            return None  # Skip highlighting if app info is unavailable

        if Seldom.debug:
            border_styles = [
                'arguments[0].style.border="3px solid #FF0000"',
                'arguments[0].style.border="3px solid #00FF00"',
                'arguments[0].style.border=""'
            ]
            for style in border_styles:
                self.browser.execute_script(style, elem)
                time.sleep(0.2)

    @property
    def info(self):
        """Return element info"""
        return self.find_elem_info

    @property
    def warn(self):
        """Return element warning"""
        return self.find_elem_warn
