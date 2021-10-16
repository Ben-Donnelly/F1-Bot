from requests import get
from datetime import datetime


class Standings:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None, driver_id=None, constructor_id=None):
		self.year = year
		self.race_number = race_number
		self.driver_id = driver_id
		self.constructor_id = constructor_id
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}

	def driver_standings_after_a_race(self):
		# This has date and time
		# TODO: Think about exact functionality wanted here, race_number defaults to last
		if not self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/driverStandings")
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/driverStandings")
		self.validate_parameters()
		print(self.def_return_value.text)
		return self.def_return_value


	def constructor_standings_after_a_race(self):
		# TODO: As above
		if not self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/constructorStandings")
		# This has date and time
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/constructorStandings")
		self.validate_parameters()
		return self


	def current_drivers_standings(self):
		self.def_return_value = get(f"{self.base_url}/current/driverStandings")
		return self


	def current_constructors_standings(self):
		self.def_return_value = get(f"{self.base_url}/current/constructorStandings")
		return self


	def all_winners_of_drivers_championships(self):
		# TODO: starts at 1950, limit = datetime current year - 1950, can offset it too and can change finishing position
		self.def_return_value = get(f"{self.base_url}/driverStandings/1?limit=25&offset=45")
		return self


	def all_winners_of_constructors_championships(self):
		# Can offset it too and can change limit
		self.def_return_value = get(f"{self.base_url}/constructorStandings/1")
		return self


	def driver_standings_by_specifying_the_driver(self):
		if not self.driver_id:
			self.message = "You need to specify a driver id"
			return self.error_message()

		self.def_return_value = get(f"{self.base_url}/drivers/{self.driver_id}/driverStandings")
		return self


	def constructor_standings_by_specifying_the_constructor(self):
		# Could limit 1 here to get first year team was in f1
		if not self.constructor_id:
			self.message = "You need to specify a constructor id"
			return self.error_message()

		self.def_return_value = get(f"{self.base_url}/constructors/{self.constructor_id}/constructorStandings")
		return self
