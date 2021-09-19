from requests import get
import json
from datetime import datetime


class Circuits:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None, driver=None):
		self.year = year
		self.driver = driver
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}

	def circuits_for_year(self):
		if self.race_number:
			data = get(f"{self.base_url}/{self.year}/{self.race_number}.json")
		else:
			data = get(f"{self.base_url}/{self.year}.json")
		self.validate_parameters()

		data = json.loads(data.text)
		races_list = data['MRData']['RaceTable']['Races']
		for race in races_list:
			print(
				f"Race {race['round']}: {race['raceName']} ({race['Circuit']['circuitName']}, {race['Circuit']['Location']['locality']}, {race['Circuit']['Location']['country']}, {race['date']}, {race['time']})")
		# print(circuits_list)
		quit()

		# TODO: Special characters (e.g. ü) print in unicode, fix
		return self
