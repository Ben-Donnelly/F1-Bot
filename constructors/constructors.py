from requests import get
import json
from datetime import datetime


class Construsctors:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None):
		self.year = year
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}

	def constructors_for_year(self):
		# There isn't much point in this? No team has ever pulled out halfway through a season?
		if self.race_number:
			data = get(f"{self.base_url}/{self.year}/{self.race_number}/constructors.json")
		else:
			data = get(f"{self.base_url}/{self.year}/constructors.json")

		data = json.loads(data.text)
		constructors_list = data['MRData']['ConstructorTable']['Constructors']
		for i in constructors_list:
			print(f"{i['name']} ({i['nationality']})")
