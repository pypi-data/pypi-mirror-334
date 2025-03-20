import os

from logging import getLogger
from selenium import webdriver
from typing import Callable
from selenium.common.exceptions import WebDriverException

logger = getLogger(__name__)


def setup_webdriver(
    user_data_dir: str = None,
    profile_dir: str = None,
    headless: bool = False,
    download_dir: str = None,
    window_position: str = "0,0",
    window_size: str = "1280,720",
    func_options: Callable[[webdriver.ChromeOptions], None] = None,
) -> webdriver.Chrome:
    """Configures and initializes a Chrome WebDriver instance.

    Args:
        user_data_dir (str, optional): Directory for storing user data. Defaults to None.
        profile_dir (str, optional): Directory for the user profile. Defaults to None.
        headless (bool, optional): If True, runs in headless mode. Defaults to False.
        download_dir (str, optional): Directory for downloaded files. Defaults to None.
        window_position (str, optional): Initial position of the browser window (e.g., "0,0"). Defaults to "0,0".
        window_size (str, optional): Size of the browser window (e.g., "1280,720"). Defaults to "1280,720".
        func_options (func, optional): A function to customize ChromeOptions. Defaults to None.

    Returns:
        webdriver.Chrome: A configured Selenium WebDriver instance for Chrome.
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    if user_data_dir:
        user_data_dir = os.path.abspath(user_data_dir)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        logger.info("user-data-dir: %s", user_data_dir)

    if profile_dir:
        options.add_argument(f"--profile-directory={profile_dir}")
        logger.info("profile-directory: %s", profile_dir)

    if headless:
        options.add_argument("--headless=new")

    if window_position:
        options.add_argument(f"--window-position={window_position}")

    if window_size:
        options.add_argument(f"--window-size={window_size}")

    if download_dir:
        download_dir = os.path.abspath(download_dir)
        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option("prefs", prefs)
        logger.info("download-directory: %s", download_dir)

    if func_options:
        func_options(options)

    try:
        service = webdriver.ChromeService()
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except WebDriverException as e:
        logger.error("Failed to initialize WebDriver: %s", e)
        raise
