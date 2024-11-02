from concurrent.futures import ProcessPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
from pathlib import Path

class Processor:
    def __init__(self, data, base_dir: Path):
        self.data = data
        self.base_dir = base_dir
        
    def process(self, key):
        logging.info(f"Processing specialization: {key}")
        self.print_lectures_table_to_file(self.data[key], file_path=self.base_dir / f"specializations/{key}/output.pmwiki")

    def print_lectures_table_to_file(self, url, file_path:Path):
        logging.info(f"Processing URL: {url}")
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        driver.get(url)
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        driver.switch_to.frame(iframe)
        table = driver.find_element(By.ID, 'EVENTLIST')
        header_row = table.find_element(By.CLASS_NAME, 'tablehead')
        headers = header_row.find_elements(By.TAG_NAME, 'th')
        column_mapping = {header.text: idx for idx, header in enumerate(headers)}
        table_data = {header.text: {} for header in headers}
        content_rows = table.find_element(By.CLASS_NAME, 'tablecontent').find_elements(By.TAG_NAME, 'tr')
        for row_idx, row in enumerate(content_rows):
            if row.value_of_css_property('display') == 'none':
                continue
            cells = row.find_elements(By.TAG_NAME, 'td')
            for column_name, idx in column_mapping.items():
                table_data[column_name][row_idx] = cells[idx].text

        # Ensure the directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w') as file:
            for row_idx in range(len(content_rows)):
                if row_idx in table_data['LV-Nr.']:
                    title = table_data['Titel'][row_idx]
                    formatted_title = title.replace('/', '_')
                    file.write(f"* [[{table_data['LV-Nr.'][row_idx]} {formatted_title} | {table_data['LV-Nr.'][row_idx]} {title}]]\n")
                    logging.info(f"Written to file: {table_data['LV-Nr.'][row_idx]} {title}")

class SpecializationsExtractor:
    def __init__(self, base_dir=Path(__file__).parent):
        self.base_dir = base_dir
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logging.basicConfig(level=logging.INFO)

    def __del__(self):
        self.driver.quit()

    def get_specializations_links(self, url):
        try:
            logging.info(f"Accessing URL: {url}")
            self.driver.get(url)
            iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'audience')))
            self.driver.switch_to.frame(iframe)
            section = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, '0xD7C07D509F5B453399672E5D323CB79B')))
            logging.info("Found the main section")

            hierarchy2_elements = []
            for sibling in section.find_elements(By.XPATH, "following-sibling::tr"):
                if 'hierarchy1' in sibling.get_attribute('class'):
                    break
                if 'hierarchy2' in sibling.get_attribute('class'):
                    hierarchy2_elements.append(sibling)
            
            data = {}
            for element in hierarchy2_elements:
                a_element = element.find_element(By.TAG_NAME, 'a')
                href = a_element.get_attribute('href')
                content = a_element.get_attribute('innerHTML')
                parts = content.split('-', 1)
                if len(parts) > 1:
                    number = parts[0].strip().split()[-1]
                    name = parts[1].strip()
                    compressed_content = f"{number} {name}"
                else:
                    compressed_content = content.strip()
                data[compressed_content] = href
                logging.info(f"Extracted link: {compressed_content} -> {href}")
            
            return data
        except Exception as e:
            logging.error(f"Error in get_specializations_links: {e}")
            return {}

    def extract_and_print_tables(self, url="https://campus.studium.kit.edu/events/audience.php#!campus/all/audience.asp?gguid=0xD7C07D509F5B453399672E5D323CB79B"):
        logging.info("Starting extraction process")
        data = self.get_specializations_links(url)
        processor = Processor(data, self.base_dir)
        with ProcessPoolExecutor() as executor:
            executor.map(processor.process, data.keys())
        logging.info("Extraction process completed")

def main():
    extractor = SpecializationsExtractor()
    extractor.extract_and_print_tables()

if __name__ == "__main__":
    main()