from requests import get
from lxml import etree
from datetime import datetime


class Calls:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number="last"):
		self.year = year
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""

	def validate_parameters(self):
		if self.race_number == 'last':
			self.extra_information = f"You did not specify a race number, so I got the information for the last race\n"

	# Drivers
	def drivers_for_year(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/drivers")
		return self

	def driver_information(self, driver_id):
		self.def_return_value = get(f"{self.base_url}/drivers/{driver_id}")
		return self

	# Constructors
	def constructors_for_year(self):
		# There isn't much point in this? No team has ever pulled out halfway through a season?
		if self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/constructors")
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/constructors")
		self.validate_parameters()
		return self

	# Circuts
	def circuts_for_year(self):
		# This is a bit more useful as it dosent seem that the circuts are in race order, but alphabetical
		if self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/circuits")
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/circuits")
		self.validate_parameters()

		# TODO: Special characters (e.g. ü) print in unicode, fix
		return self

	# result
	def results(self):
		# This is cool
		# Most recent race result: replace year and race_number with current and last
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/results")
		self.validate_parameters()
		return self

	# Seasons
	# Ignore the type hint here
	def schedule_for_year(self):
		# This has date and time
		# Can do year = "current"
		self.def_return_value = get(f"{self.base_url}/{self.year}")
		return self

	def season_list(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}")
		return self

	# Qualifying
	def qualifying_results(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/qualifying")
		self.validate_parameters()
		return self

	# Standings
	def driver_standings_after_a_race(self):
		# This has date and time
		if not self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/driverStandings")
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/driverStandings")
		self.validate_parameters()
		return self

	def constructor_standings_after_a_race(self):
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

	def driver_standings_by_specifying_the_driver(self, driver_id):
		self.def_return_value = get(f"{self.base_url}/drivers/{driver_id}/driverStandings")
		return self

	def constructor_standings_by_specifying_the_constructor(self, constructor_id):
		# Could limit 1 here to get first year team was in f1
		self.def_return_value = get(f"{self.base_url}/constructors/{constructor_id}/constructorStandings")
		return self

	# Finishing status
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
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/status")
		self.validate_parameters()
		return self

	# Lap times
	def lap_times(self, lapnumber=None):
		# Maybe not the best idea to not specify lapnumber as returns > 1000 results
		# Leaving in for now
		get_url = f"{self.base_url}/{self.year}/{self.race_number}/laps"
		if lapnumber:
			get_url += f"/{lapnumber}"

		self.def_return_value = get(get_url)
		self.validate_parameters()
		return self

	# Pit stops
	def pit_stop_data_for_a_race(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/pitstops")
		self.validate_parameters()
		return self

	def specific_pit_stop_data_for_a_race(self, pitstop_number):
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/pitstops/{pitstop_number}")
		self.validate_parameters()
		return self

	@staticmethod
	def to_string(data):
		to_string_return_value = etree.fromstring(data.def_return_value.content)
		return f"{data.extra_information}{etree.tostring(to_string_return_value, pretty_print=True).decode()}"

	@staticmethod
	def main():
		# noinspection PyTypeChecker
		api_call = Calls(race_number=4)

		api_call_result = api_call.drivers_for_year()

		print(api_call.to_string(api_call_result))


if __name__ == "__main__":
	call = Calls()
	call.main()
