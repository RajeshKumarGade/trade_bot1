import os
import time

from kiteconnect import KiteConnect
from pyotp import TOTP
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from auth.credentials import read_credentials
from config.settings import ACCESS_TOKEN_FILE, DATA_DIR


def _first_visible_element(driver, selectors, timeout=20):
    wait = WebDriverWait(driver, timeout)
    for by, value in selectors:
        try:
            element = wait.until(EC.visibility_of_element_located((by, value)))
            return element
        except Exception:
            continue
    raise RuntimeError(f"Could not find any selector: {selectors}")


def _dump_debug_artifacts(driver):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    html_path = DATA_DIR / "selenium_debug_page.html"
    png_path = DATA_DIR / "selenium_debug_page.png"
    try:
        html_path.write_text(driver.page_source, encoding="utf-8")
    except Exception:
        pass
    try:
        driver.save_screenshot(str(png_path))
    except Exception:
        pass
    print(f"Saved Selenium debug artifacts to: {html_path} and {png_path}")


def generate_access_token():
    key_secret = read_credentials()
    if len(key_secret) < 5 or not key_secret[2] or not key_secret[3] or not key_secret[4]:
        raise ValueError(
            "Auto login requires KITE_USER_ID/KITE_PASSWORD/KITE_TOTP_SECRET or full api_key.txt fields."
        )

    kite = KiteConnect(api_key=key_secret[0])
    chrome_driver_path = os.getenv("CHROMEDRIVER_PATH")
    chrome_binary_path = os.getenv("CHROME_BIN")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if chrome_binary_path:
        options.binary_location = chrome_binary_path

    if chrome_driver_path:
        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    try:
        driver.get(kite.login_url())
        wait = WebDriverWait(driver, 25)

        user_input = _first_visible_element(
            driver,
            [
                (By.XPATH, '//input[@type="text"]'),
                (By.CSS_SELECTOR, 'input[autocomplete="username"]'),
            ],
        )
        user_input.clear()
        user_input.send_keys(key_secret[2])

        password_input = _first_visible_element(
            driver,
            [
                (By.XPATH, '//input[@type="password"]'),
                (By.CSS_SELECTOR, 'input[autocomplete="current-password"]'),
            ],
        )
        password_input.clear()
        password_input.send_keys(key_secret[3])

        login_button = _first_visible_element(
            driver,
            [
                (By.XPATH, '//button[@type="submit"]'),
                (By.CSS_SELECTOR, "button"),
            ],
        )
        login_button.click()

        totp = TOTP(key_secret[4]).now()
        totp_input = _first_visible_element(
            driver,
            [
                (By.CSS_SELECTOR, 'input[autocomplete="one-time-code"]'),
                (By.XPATH, '//input[@type="tel"]'),
                (By.XPATH, '//input[@type="number"]'),
                (By.XPATH, '//input[@type="password"]'),
            ],
            timeout=30,
        )
        totp_input.clear()
        totp_input.send_keys(totp)

        verify_button = _first_visible_element(
            driver,
            [
                (By.XPATH, '//button[@type="submit"]'),
                (By.CSS_SELECTOR, "button"),
            ],
        )
        verify_button.click()

        wait.until(lambda d: "request_token=" in d.current_url)
        request_token = driver.current_url.split("request_token=")[1][:32]

        session_data = kite.generate_session(request_token, api_secret=key_secret[1])
        access_token = session_data["access_token"]

        with open(ACCESS_TOKEN_FILE, "w") as file:
            file.write(access_token)

        print("Access token generated successfully")
        return access_token
    except Exception:
        _dump_debug_artifacts(driver)
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass
