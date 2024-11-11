import os
import tempfile
import time
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from ilias.login import Login


class DriverManager:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir

    def __enter__(self):
        options = Options()

        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": str(self.temp_dir),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "plugins.always_open_pdf_externally": True,
            },
        )
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


class PdfDownloader:
    def __init__(self, download_dir: Path):
        self.download_dir = download_dir
        self.url_login = (
            "https://ilias.studium.kit.edu/login.php?"
            "client_id=produktiv&cmd=force_login&lang=de"
        )
        # Load environment variables from passwords.env file
        load_dotenv(dotenv_path="passwords.env")
        # Get username and password from environment variables
        self.username = os.getenv("ILIAS_USERNAME")
        self.password = os.getenv("ILIAS_PASSWORD")

    def download(self, url: str):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp_dir:
            with DriverManager(temp_dir) as driver:
                return self._download(Path(temp_dir), driver, url)

    def _download(self, temp_dir: Path, driver: WebDriver, url: str):
        if not Login().login(driver):
            return None
        driver.get(url)

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
        return pdf_file_dest
