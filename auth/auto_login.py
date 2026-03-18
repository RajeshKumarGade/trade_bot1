import os
import time

from kiteconnect import KiteConnect
from pyotp import TOTP
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from auth.credentials import read_credentials
from config.settings import ACCESS_TOKEN_FILE


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

    driver.get(kite.login_url())
    driver.implicitly_wait(10)

    driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(key_secret[2])
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(key_secret[3])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(2)
    totp = TOTP(key_secret[4]).now()
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(totp)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(8)
    request_token = driver.current_url.split("request_token=")[1][:32]
    driver.quit()

    session_data = kite.generate_session(request_token, api_secret=key_secret[1])
    access_token = session_data["access_token"]

    with open(ACCESS_TOKEN_FILE, "w") as file:
        file.write(access_token)

    print("Access token generated successfully")
    return access_token
