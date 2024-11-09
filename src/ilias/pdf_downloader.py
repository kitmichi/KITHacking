import os
import tempfile
import time
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class PdfDownloader:
    def __init__(self, download_dir: Path, url: str):
        self.download_dir = download_dir
        self.url = url
        # Load environment variables from passwords.env file
        load_dotenv(dotenv_path="passwords.env")
        # Get username and password from environment variables
        self.username = os.getenv("ILIAS_USERNAME")
        self.password = os.getenv("ILIAS_PASSWORD")

    def download(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp_dir:
            return self.d2(Path(temp_dir))

    def d2(self, temp_dir: Path):
        options = Options()

        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": str(temp_dir),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "plugins.always_open_pdf_externally": True,
            },
        )
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        # Open the HTML file in the browser
        driver.get(self.url)
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

        if login_cookie_set:
            driver.get(
                "https://ilias.studium.kit.edu/ilias.php?"
                "baseClass=ilrepositorygui&cmd=sendfile&ref_id=2512118"
            )

            # Function to wait for the file to exist
            def wait_for_file_to_exist(file_path: Path, timeout=30):
                start_time = time.time()
                while time.time() - start_time < timeout:
                    pdf_files = [file.name for file in file_path.glob("*.pdf")]
                    if pdf_files:
                        print(f"File {pdf_files[0]} exists.")
                        return file_path / pdf_files[0]
                    time.sleep(1)
                print(f"Timeout: File {pdf_files[0]} does not exist.")
                return None

            # Wait for the file to be downloaded
            pdf_file = wait_for_file_to_exist(temp_dir)
            pdf_file_dest = self.download_dir / pdf_file.name
            pdf_file.rename(pdf_file_dest)

        # Close the browser
        driver.quit()
        return pdf_file_dest
