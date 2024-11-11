import os
import time

from dotenv import load_dotenv
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Login:
    def __init__(self):
        self.url_login = (
            "https://ilias.studium.kit.edu/login.php?"
            "client_id=produktiv&cmd=force_login&lang=de"
        )
        # Load environment variables from passwords.env file
        load_dotenv(dotenv_path="passwords.env")
        # Get username and password from environment variables
        self.username = os.getenv("ILIAS_USERNAME")
        self.password = os.getenv("ILIAS_PASSWORD")

    def login(self, driver: WebDriver):
        # Open the HTML file in the browser
        driver.get(self.url_login)
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "button_shib_login"))
        )
        login_button.click()

        username_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_text.send_keys(self.username)

        password_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_text.send_keys(self.password)

        sbmt_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sbmt"))
        )
        sbmt_button.click()

        # Function to check if the login cookie is set
        def is_login_cookie_set(driver, cookie_name):
            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie["name"] == cookie_name:
                    return True
            return False

        # Wait until the login cookie is set
        cookie_name = "PHPSESSID"
        timeout = 30  # Timeout in seconds
        start_time = time.time()

        while time.time() - start_time < timeout:
            login_cookie_set = is_login_cookie_set(driver, cookie_name)
            if login_cookie_set:
                print("Login cookie is set.")
                break
            time.sleep(1)
        else:
            print("Timeout: Login cookie was not set.")
        return login_cookie_set
