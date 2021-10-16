from requests import get

from datetime import datetime


class PitStops:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None, pitstop_number=None):
		self.year = year
		self.race_number = race_number
		self.pitstop_number = pitstop_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}

	def pit_stop_data_for_a_race(self):
		if not self.race_number:
			self.race_number = 'last'

		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/pitstops")
		self.validate_parameters()
		return self


	def specific_pit_stop_data_for_a_race(self):
		if not self.pitstop_number:
			self.message = "You need to specify a constructor id"
			return self.error_message()

		if not self.race_number:
			self.race_number = 'last'
		# Todo: if no pitstop number
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/pitstops/{self.pitstop_number}")
		self.validate_parameters()
		return self
