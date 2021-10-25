from requests import get
from datetime import datetime
import ApiCalls


class Qualifying:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None):
		self.year = year
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}
		self.api_call = ApiCalls.Call()

	def qualifying_results(self):
		if not self.race_number:
			self.race_number = 'last'

		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/qualifying")
		self.api_call.validate_parameters()
		return self
