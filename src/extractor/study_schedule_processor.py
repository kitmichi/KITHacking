from tqdm import tqdm
from selenium.webdriver.common.by import By

class StudyPlanProcessor:
	def __init__(self):
		self.study_schedule = {}
		self.current_study = None
		self.current_section = None
		self.current_module = None
		self.current_brick = None

	def get_container(self, hierarchy_class, titel):
		if hierarchy_class == 'hierarchy1':
			self.current_study = titel
			return self.study_schedule
		elif hierarchy_class == 'hierarchy2':
			self.current_section = titel
			return self.study_schedule.setdefault(self.current_study, {})
		elif hierarchy_class == 'hierarchy3':
			self.current_module = titel
			return self.study_schedule.setdefault(self.current_study, {}).setdefault(self.current_section, {})
		elif hierarchy_class == 'hierarchy4':
			self.current_brick = titel
			return self.study_schedule.setdefault(self.current_study, {}).setdefault(self.current_section, {}).setdefault(self.current_module, {})
		return None

	def process_rows(self, rows):
		for row in tqdm(rows, desc="Processing rows"):
			hierarchy_class = [cls for cls in row.get_attribute('class').split() if 'hierarchy' in cls][0]  # Get the hierarchy level from class attribute
			cells = row.find_elements(By.TAG_NAME, 'td')
			if len(cells) > 1:
				titel = cells[1].text.strip()
				type = cells[2].text.strip()
				CP = cells[3].text.strip()
				link_tag = cells[1].find_element(By.TAG_NAME, 'a')
				link = link_tag.get_attribute('href') if link_tag else None

				container = self.get_container(hierarchy_class, titel)
				if container is not None:
					container[titel] = {
						"type": type,
						"CP": CP,
						"link": link,
					}