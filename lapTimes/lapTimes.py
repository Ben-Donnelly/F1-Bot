from requests import get
from datetime import datetime

class LapTimes:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None, driver=None, lapnumber=None):
		self.year = year
		self.driver = driver
		self.race_number = race_number
		self.lapnumber = lapnumber
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}
	def lap_times(self):
		# Maybe not the best idea to not specify lapnumber as returns > 1000 results
		# Leaving in for now
		if not self.race_number:
			self.race_number = 'last'

		get_url = f"{self.base_url}/{self.year}/{self.race_number}/laps"
		if self.lapnumber:
			get_url += f"/{self.lapnumber}"

		self.def_return_value = get(get_url)
		self.validate_parameters()
		return self
