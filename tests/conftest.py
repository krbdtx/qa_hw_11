import os
from selene import browser
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import attach
from dotenv import load_dotenv

DEFAULT_BROWSER_VERSION = "100.0"


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='100.0'
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    options = Options()
    selenoid_capabilities = {
        "browserName": 'chrome',
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    login = os.getenv('SELENOID_LOGIN')
    password = os.getenv('SELENOID_PASS')
    selenoid_url = os.getenv('SELENOID_URL')

    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@{selenoid_url}",
        options=options
    )

    browser.config.base_url = 'https://demoqa.com'
    browser.config.window_width = 768
    browser.config.window_height = 1366
    browser.config.driver = driver

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()
