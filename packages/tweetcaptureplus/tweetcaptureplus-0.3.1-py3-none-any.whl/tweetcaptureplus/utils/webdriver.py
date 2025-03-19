from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .utils import get_chromedriver_default_path
from os.path import exists
from os import environ


async def get_driver(custom_options=None, driver_path=None, gui=False):
    chrome_options = Options()
    if gui is False:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=788,788")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.35 Safari/537.36")

    if isinstance(custom_options, list) and len(custom_options) > 0:
        for option in custom_options:
            chrome_options.add_argument(option)

    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # CHROME_DRIVER environment variable : priority 1
    if environ.get("CHROME_DRIVER") is not None:
        try:
            driver = webdriver.Chrome(
                service=Service(executable_path=environ.get("CHROME_DRIVER")),
                options=chrome_options,
            )
            return driver
        except Exception as e:
            print(e)
            pass

    # driver_path argument : priority 2
    if driver_path is None:
        driver_path = get_chromedriver_default_path()
    if exists(driver_path):
        try:
            driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=chrome_options)
            return driver
        except Exception as e:
            print(e)
            pass

    # webdriver-manager : priority 3
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver
    except Exception as e:
        print(e)
        pass

    return None
