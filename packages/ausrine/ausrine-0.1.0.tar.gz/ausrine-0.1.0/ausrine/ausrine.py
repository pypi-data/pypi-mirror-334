import time

from logging import DEBUG, getLogger
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    ElementNotInteractableException,
)

DEFAULT_TIMEOUT = 10.0

logger = getLogger(__name__)

special_keys_codes = [
    Keys.NULL,
    Keys.CANCEL,
    Keys.HELP,
    Keys.BACKSPACE,
    Keys.BACK_SPACE,
    Keys.TAB,
    Keys.CLEAR,
    Keys.RETURN,
    Keys.ENTER,
    Keys.SHIFT,
    Keys.LEFT_SHIFT,
    Keys.CONTROL,
    Keys.LEFT_CONTROL,
    Keys.ALT,
    Keys.LEFT_ALT,
    Keys.PAUSE,
    Keys.ESCAPE,
    Keys.SPACE,
    Keys.PAGE_UP,
    Keys.PAGE_DOWN,
    Keys.END,
    Keys.HOME,
    Keys.LEFT,
    Keys.ARROW_LEFT,
    Keys.UP,
    Keys.ARROW_UP,
    Keys.RIGHT,
    Keys.ARROW_RIGHT,
    Keys.DOWN,
    Keys.ARROW_DOWN,
    Keys.INSERT,
    Keys.DELETE,
    Keys.SEMICOLON,
    Keys.EQUALS,
    Keys.NUMPAD0,
    Keys.NUMPAD1,
    Keys.NUMPAD2,
    Keys.NUMPAD3,
    Keys.NUMPAD4,
    Keys.NUMPAD5,
    Keys.NUMPAD6,
    Keys.NUMPAD7,
    Keys.NUMPAD8,
    Keys.NUMPAD9,
    Keys.MULTIPLY,
    Keys.ADD,
    Keys.SEPARATOR,
    Keys.SUBTRACT,
    Keys.DECIMAL,
    Keys.DIVIDE,
    Keys.F1,
    Keys.F2,
    Keys.F3,
    Keys.F4,
    Keys.F5,
    Keys.F6,
    Keys.F7,
    Keys.F8,
    Keys.F9,
    Keys.F10,
    Keys.F11,
    Keys.F12,
    Keys.META,
    Keys.COMMAND,
    Keys.ZENKAKU_HANKAKU,
]


class WebAutomationDriver:
    def __init__(self, webdriver: WebDriver) -> None:
        """Initialize the WebAutomationDriver.

        Args:
            webdriver (WebDriver): An instance of WebDriver.
        """
        self.webdriver = webdriver
        self.debug = logger.level <= DEBUG

    def quit(self):
        """Quits the driver and closes every associated window.

        Usage:
            ausrine = WebAutomationDriver(webdriver)

            ausrine.quit()
        """
        self.webdriver.quit()

    def get(
        self,
        url: str,
        prewait: float = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Loads a web page in the current browser session.

        Args:
            url (str): The URL to load.
            prewait (float, optional): Time to wait before executing the action in seconds. Defaults to None.
            timeout (float, optional): Maximum wait time, in seconds. Defaults to 10.0.

        Raises:
            TimeoutException: If the page load times out.
            WebDriverException: If a WebDriver-related error occurs.
        """
        if url is None:
            raise ValueError("get: 'url' parameter is required")

        try:
            logger.info("get: %s", url)
            if prewait:
                time.sleep(prewait)
            self.webdriver.get(url)
            WebDriverWait(self.webdriver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException as e:
            logger.error("get: timeout: url=%s", url)
            raise e
        except WebDriverException as e:
            logger.error("get: WebDriverException: url=%s: %s", url, e)
            raise e

    def _parse_get_from(self, map: dict):
        self.get(
            url=map.get("url"),
            prewait=map.get("prewait"),
            timeout=map.get("timeout", DEFAULT_TIMEOUT),
        )

    def wait_until_find_element(
        self,
        by: str,
        value: str,
        prewait: float = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> WebElement:
        """Find an element given a By strategy and locator.

        Args:
            by (str): The Selenium By strategy (e.g., By.ID, By.XPATH).
            value (str): The locator value to find the element.
            prewait (float, optional): Time to wait before executing the action in seconds. Defaults to None.
            timeout (float, optional): Maximum wait time, in seconds. Defaults to 10.0.

        Returns:
            WebElement: The found web element.
        """
        if prewait:
            time.sleep(prewait)

        element = WebDriverWait(self.webdriver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

        return element

    def click(
        self,
        by: str,
        value: str,
        prewait: float = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Clicks an element found using a locator strategy.

        Args:
            by (str): The Selenium By strategy (e.g., By.ID, By.XPATH).
            value (str): The locator value to find the element.
            prewait (float, optional): Time to wait before executing the action in seconds. Defaults to None.
            timeout (float, optional): Maximum wait time, in seconds. Defaults to 10.0.

        Raises:
            TimeoutException: If the element is not found within the timeout.
            ElementNotInteractableException: If an element cannot be interacted with.
        """

        if by is None:
            raise ValueError("click: 'by' parameter is required")
        if value is None:
            raise ValueError("click: 'value' parameter is required")

        try:
            logger.info("click: by=%s, value=%s", by, value)
            e = self.wait_until_find_element(by, value, prewait, timeout)
            if self.debug:
                logger.debug("click: outerHTML: %s", e.get_attribute("outerHTML"))
            e.click()
        except TimeoutException as e:
            logger.error("click: timeout: by=%s, value=%s", by, value)
            raise e
        except ElementNotInteractableException as e:
            logger.error("click: element not interactable: by=%s, value=%s", by, value)
            raise e

    def _parse_click_from(self, map: dict):
        self.click(
            by=map.get("by"),
            value=map.get("value"),
            prewait=map.get("prewait"),
            timeout=map.get("timeout", DEFAULT_TIMEOUT),
        )

    def submit(
        self,
        by: str,
        value: str,
        prewait: float = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Submits a form element found using a locator strategy.

        Args:
            by (str): The Selenium By strategy (e.g., By.ID, By.XPATH).
            value (str): The locator value to find the element.
            prewait (float, optional): Time to wait before executing the action in seconds. Defaults to None.
            timeout (float, optional): Maximum wait time, in seconds. Defaults to 10.0.

        Raises:
            TimeoutException: If the element is not found within the timeout.
            ElementNotInteractableException: If an element cannot be interacted with.
        """
        if by is None:
            raise ValueError("submit: 'by' parameter is required")
        if value is None:
            raise ValueError("submit: 'value' parameter is required")

        try:
            logger.info("submit: by=%s, value=%s", by, value)
            e = self.wait_until_find_element(by, value, prewait, timeout)
            if self.debug:
                logger.debug("submit: outerHTML: %s", e.get_attribute("outerHTML"))
            e.submit()
        except TimeoutException as e:
            logger.error("submit: timeout: by=%s, value=%s", by, value)
            raise e
        except ElementNotInteractableException as e:
            logger.error("submit: element not interactable: by=%s, value=%s", by, value)
            raise e

    def _parse_submit_from(self, map: dict):
        self.submit(
            by=map.get("by"),
            value=map.get("value"),
            prewait=map.get("prewait"),
            timeout=map.get("timeout", DEFAULT_TIMEOUT),
        )

    def clear(
        self,
        by: str,
        value: str,
        prewait: float = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Clears the text of an element found using a locator strategy.

        Args:
            by (str): The Selenium By strategy (e.g., By.ID, By.XPATH).
            value (str): The locator value to find the element.
            prewait (float, optional): Time to wait before executing the action in seconds. Defaults to None.
            timeout (float, optional): Maximum wait time, in seconds. Defaults to 10.0.

        Raises:
            TimeoutException: If the element is not found within the timeout.
            ElementNotInteractableException: If an element cannot be interacted with.
        """
        if by is None:
            raise ValueError("clear: 'by' parameter is required")
        if value is None:
            raise ValueError("clear: 'value' parameter is required")

        try:
            logger.info("clear: by=%s, value=%s", by, value)
            e = self.wait_until_find_element(by, value, prewait, timeout)
            if self.debug:
                logger.debug("clear: outerHTML: %s", e.get_attribute("outerHTML"))
            e.clear()
        except TimeoutException as e:
            logger.error("clear: timeout: by=%s, value=%s", by, value)
            raise e
        except ElementNotInteractableException as e:
            logger.error("clear: element not interactable: by=%s, value=%s", by, value)
            raise e

    def _parse_clear_from(self, map: dict):
        self.clear(
            by=map.get("by"),
            value=map.get("value"),
            prewait=map.get("prewait"),
            timeout=map.get("timeout", DEFAULT_TIMEOUT),
        )

    def send_keys(
        self,
        by: str,
        value: str,
        text: str | Keys,
        password: bool = False,
        append: bool = False,
        prewait: float = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Sends keys to an element found using a locator strategy.

        Args:
            by (str): The Selenium By strategy (e.g., By.ID, By.XPATH).
            value (str): The locator value to find the element.
            text (str | Keys): A string to type or a special key like Keys.ENTER.
            password (bool, optional): If set to True, the text is treated as a password.
            append (bool, optional): If set to True, text is appended to the textbox.
            prewait (float, optional): Time to wait before executing the action in seconds. Defaults to None.
            timeout (float, optional): Maximum wait time, in seconds. Defaults to 10.0.

        Raises:
            TimeoutException: If the element is not found within the timeout.
            ElementNotInteractableException: If an element cannot be interacted with.
        """
        if by is None:
            raise ValueError("send_keys: 'by' parameter is required")
        if value is None:
            raise ValueError("send_keys: 'value' parameter is required")
        if text is None:
            raise ValueError("send_keys: 'text' parameter is required")

        try:
            if password:
                logger.info("send_keys: by=%s, value=%s, text=password", by, value)
            elif text in special_keys_codes:
                logger.info("send_keys: by=%s, value=%s, text=special_key", by, value)
            else:
                logger.info("send_keys: by=%s, value=%s, text=%s", by, value, text)
            e = self.wait_until_find_element(by, value, prewait, timeout)
            if self.debug:
                logger.debug("send_keys: outerHTML: %s", e.get_attribute("outerHTML"))

            # If 'append' is True or 'text' is an instance of Keys (special key like Keys.ENTER),
            # send the keys directly to the element without clearing it.
            if (append) or (text in special_keys_codes):
                e.send_keys(text)
            else:
                # Otherwise, clear the element before sending the keys.
                e.clear()
                e.send_keys(text)
        except TimeoutException as e:
            logger.error("send_keys: timeout: by=%s, value=%s", by, value)
            raise e
        except ElementNotInteractableException as e:
            logger.error(
                "send_keys: element not interactable: by=%s, value=%s", by, value
            )
            raise e

    def _parse_send_keys_from(self, map: dict):
        self.send_keys(
            by=map.get("by"),
            value=map.get("value"),
            text=map.get("text"),
            password=map.get("password", False),
            append=map.get("append", False),
            prewait=map.get("prewait"),
            timeout=map.get("timeout", DEFAULT_TIMEOUT),
        )

    def execute(self, sequences: list[dict]) -> None:
        """Executes a sequence of web automation commands.

        Args:
            sequences (list[dict]): A list of dictionaries defining commands to execute.

        Raises:
            WebDriverException: If a WebDriver-related error occurs.
            TimeoutException: If an element is not found within the timeout.
            ElementNotInteractableException: If an element cannot be interacted with.
            ValueError: If a command is unrecognized or missing required parameters.

        Usage:
            sequences = [
                {"get": {"url": "https://www.google.com"}},
                {"click": {"by": By.XPATH, "value": "//textarea[@title='Search']"}},
                {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']", "text": "iphone"}},
                {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']", "text": Keys.ENTER}},
            ]
            ausrine = WebAutomationDriver(webdriver)
            ausrine.execute(sequences)
        """
        for seq in sequences:
            for k, v in seq.items():
                match k.lower():
                    case "get":
                        self._parse_get_from(v)
                    case "click":
                        self._parse_click_from(v)
                    case "submit":
                        self._parse_submit_from(v)
                    case "clear":
                        self._parse_clear_from(v)
                    case "send_keys":
                        self._parse_send_keys_from(v)
                    case _:
                        logger.error("execute: unrecognized command: '%s'", k)
                        raise ValueError(f"execute: unrecognized command: '{k}'")

    def try_execute(self, sequences: list[dict]) -> Optional[Exception]:
        """Tries to execute a sequence of web automation commands.

        Args:
            sequences (list[dict]): List of command sequences to execute.

        Returns:
            Optional[Exception]: Returns an Exception if an error occurs during execution
            or None if no error occurs.

        Usage:
            sequences = [
                {"get": {"url": "https://www.google.com"}},
                {"click": {"by": By.XPATH, "value": "//textarea[@title='Search']"}},
                {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']", "text": "iphone"}},
                {"send_keys": {"by": By.XPATH, "value": "//textarea[@title='Search']", "text": Keys.ENTER}},
            ]
            ausrine = WebAutomationDriver(webdriver)
            error = ausrine.try_execute(sequences)
            if error:
                # Handle the error
            else:
                # Continue with the next steps
        """
        error = None

        try:
            self.execute(sequences)
        except (
            WebDriverException,
            TimeoutException,
            ElementNotInteractableException,
            ValueError,
        ) as e:
            logger.error("try_execute: %s: %s", type(e).__name__, e)
            error = e

        return error
