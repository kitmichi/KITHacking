from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from .study_plan_processor import StudyPlanProcessor

def get_study_plan():
	# URL to be fetched
	url = "https://campus.studium.kit.edu/events/audience.php#!campus/all/abstractStudyScheduleView.asp?gguid=0xF654B5E6CC6842A8B943858D89F69741&capvguid=0x32F8959548FE4CE8A0EA1FCE19956FB7"

	# Initialize the WebDriver
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	# Open the URL
	driver.get(url)

	# Wait for the iframe to be present and switch to it
	iframe = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
	)
	driver.switch_to.frame(iframe)

	# Extract rows from the table based on hierarchy class
	rows = driver.find_elements(By.CSS_SELECTOR, 'tr[class*="hierarchy"]')
	processor = StudyPlanProcessor()
	processor.process_rows(rows)

	# Close the WebDriver
	driver.quit()
	return processor.study_plan

# Function to convert JSON to PmWiki table with simulated indentation and special formatting for keys containing "T-ETIT-"
def study_plan_to_pmwiki_table(data):
    pmwiki = "||!Key ||!Art ||!LP ||!Link ||\n"
    def process_item(key, value, indent=0):
        nonlocal pmwiki
        indent_spaces = " " * indent
        if isinstance(value, dict):
            art = value.get("art", "")
            lp = value.get("LP", "")
            link = value.get("link", "")
            if str(key).startswith("T-"):
                key = f"[[{key.replace("/", "_")} | {key}]]"
            pmwiki += f"||{indent_spaces}{key} ||{art} ||{lp} ||[[{link} | link]] ||\n"
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    process_item(sub_key, sub_value, indent + 4)
        elif isinstance(value, list):
            for item in value:
                process_item(key, item, indent)
        else:
            pmwiki += f"||{indent_spaces}{key} || || || ||\n"
    for key, value in data.items():
        process_item(key, value)
    return pmwiki

if __name__ == "__main__":
	study_plan = get_study_plan()

	# Convert JSON to PmWiki table
	pmwiki_table = study_plan_to_pmwiki_table(study_plan)

	# Path to save the PmWiki table file
	pmwiki_file_path = Path(__file__).parent / 'study_plan_with_links.pmwiki'

	# Save the PmWiki table to a file
	with open(pmwiki_file_path, 'w') as file:
		file.write(pmwiki_table)

	print(f"The study plan has been successfully converted to a PmWiki table format and saved to '{pmwiki_file_path}'.")
