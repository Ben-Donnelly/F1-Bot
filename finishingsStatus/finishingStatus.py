from requests import get
from datetime import datetime
import ApiCalls


class FinishingStatus:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None):
		self.year = year
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}

	def list_of_all_finishing_status_codes(self):
		# There's 135 status codes here so far but just set to 150
		# Basically tells you how many times drivers have finished, been disqualified, injured etc.
		# Could merge with 2 methods below

		self.def_return_value = get(f"{self.base_url}/status?limit=150")
		return self


	def list_of_finishing_status_for_a_specific_season(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/status")
		return self


	def list_of_finishing_status_for_a_specific_race_number_in_a_season(self):
		if not self.race_number:
			self.race_number = 'last'

		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/status")

		ApiCall = ApiCalls.Call()
		ApiCall.validate_parameters()
		return self
