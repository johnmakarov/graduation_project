import os
import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tests.utils import attach


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="local",
        help="Выбор браузера: local, selenoid",
    )


@pytest.fixture(scope="function", autouse=True)
def browser_context(request):
    browser_type = request.config.getoption("--browser")

    if browser_type == "selenoid":
        yield from selenoid_fixture()
    else:
        yield from local_fixture()

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)

    if browser_type == "selenoid":
        attach.add_video(browser)

    browser.quit()


def local_fixture():
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = "eager"
    browser.config.driver_options = driver_options
    browser.config.window_width = 1100
    browser.config.window_height = 1080
    browser.config.base_url = "https://uralsib.ru/"
    browser.open(browser.config.base_url)

    yield browser


def selenoid_fixture():
    options = Options()

    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "127.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "enableLog": True,
            "logName": "browser.log",
        },
    }

    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
        options=options,
    )

    browser.config.driver = driver
    browser.config.window_width = 1100
    browser.config.window_height = 1080
    browser.config.base_url = "https://uralsib.ru/"
    browser.open()

    yield browser


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture()
def api_url():
    browser.config.base_url = "https://uralsib.ru/"
    return browser.config.base_url
