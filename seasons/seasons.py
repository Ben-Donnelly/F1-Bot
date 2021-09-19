from requests import get
from datetime import datetime


class Seasons:
	current_year = datetime.today().year

	def __init__(self, year=current_year):
		self.year = year
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}


	def schedule_for_year(self):
		# This has date and time
		# Can do year = "current"
		self.def_return_value = get(f"{self.base_url}/{self.year}")
		return self


	def season_list(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}")

		return self
