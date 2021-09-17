from requests import get
from lxml import etree
from datetime import datetime


class APICalls:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number="last"):
		self.year = year
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""

	# Drivers
	def drivers_for_year(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/drivers")
		return self.to_string()

	def driver_information(self, driver_id):
		self.def_return_value = get(f"{self.base_url}/drivers/{driver_id}")
		return self.to_string()

	# Constructors
	def constructors_for_year(self):
		# There isn't much point in this? No team has ever pulled out halfway through a season?
		if self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/constructors")
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/constructors")
		return self.to_string()

	# Circuts
	def circuts_for_year(self):
		# This is a bit more useful as it dosent seem that the circuts are in race order, but alphabetical
		if self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/circuits")
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/circuits")
		# TODO: Special characters (e.g. ü) print in unicode, fix
		return self.to_string()

	# result
	def results(self):
		# This is cool
		# Most recent race result: replace year and race_number with current and last
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/results")
		if self.race_number == 'last':
			self.extra_information = "You did not specifY a race number so I got the information for the last race\n"
		return self.to_string()

	# Seasons
	# Ignore the type hint here
	def schedule_for_year(self):
		# This has date and time
		# Can do year = "current"
		self.def_return_value = get(f"{self.base_url}/{self.year}")
		return self.to_string()

	def season_list(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}")
		return self.to_string()

	# Qualifying
	def qualifying_results(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/qualifying")
		return self.to_string()

	# Standings
	def driver_standings_after_a_race(self):
		# This has date and time
		if not self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/driverStandings")
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/driverStandings")
		return self.to_string()

	def constructor_standings_after_a_race(self):
		if not self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/constructorStandings")
		# This has date and time
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/constructorStandings")
		return self.to_string()

	def current_drivers_standings(self):
		self.def_return_value = get(f"{self.base_url}/current/driverStandings")
		return self.to_string()

	def current_constructors_standings(self):
		self.def_return_value = get(f"{self.base_url}/current/constructorStandings")
		return self.to_string()

	def all_winners_of_drivers_championships(self):
		# TODO: starts at 1950, limit = datetime current year - 1950, can offset it too and can change finishing position
		self.def_return_value = get(f"{self.base_url}/driverStandings/1?limit=25&offset=45")
		return self.to_string()

	def all_winners_of_constructors_championships(self):
		# Can offset it too and can change limit
		self.def_return_value = get(f"{self.base_url}/constructorStandings/1")
		return self.to_string()

	def driver_standings_by_specifying_the_driver(self, driver_id):
		self.def_return_value = get(f"{self.base_url}/drivers/{driver_id}/driverStandings")
		return self.to_string()

	def constructor_standings_by_specifying_the_constructor(self, constructor_id):
		# Could limit 1 here to get first year team was in f1
		self.def_return_value = get(f"{self.base_url}/constructors/{constructor_id}/constructorStandings")
		return self.to_string()

	# Finishing status
	def list_of_all_finishing_status_codes(self):
		# There's 135 status codes here so far but just set to 150
		# Basically tells you how many times drivers have finished, been disqualified, injured etc.
		# Could merge with 2 methods below

		self.def_return_value = get(f"{self.base_url}/status?limit=150")
		return self.to_string()

	def list_of_finishing_status_for_a_specific_season(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/status")
		return self.to_string()

	def list_of_finishing_status_for_a_specific_race_number_in_a_season(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/status")
		return self.to_string()

	# Lap times
	def lap_times(self, lapnumber=None):
		# Maybe not the best idea to not specify lapnumber as returns > 1000 results
		# Leaving in for now
		get_url = f"{self.base_url}/{self.year}/{self.race_number}/laps"
		if lapnumber:
			get_url += f"/{lapnumber}"

		self.def_return_value = get(get_url)
		return self.to_string()

	# Pit stops
	def pit_stop_data_for_a_race(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/pitstops")
		return self.to_string()

	def specific_pit_stop_data_for_a_race(self, pitstop_number):
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/pitstops/{pitstop_number}")
		return self.to_string()

	def to_string(self):
		to_string_return_value = etree.fromstring(self.def_return_value.content)
		return f"{self.extra_information}{etree.tostring(to_string_return_value, pretty_print=True).decode()}"

	@staticmethod
	def main():
		api_call = APICalls()
		# Next: All winners of drivers' championships
		print(api_call.results())


if __name__ == "__main__":
	api_call = APICalls()
	api_call.main()
