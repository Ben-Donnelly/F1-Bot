from requests import get
from lxml import etree
from datetime import datetime


class APICalls:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None):
		self.year = year
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1/"

	# Drivers
	def drivers_for_year(self):
		drivers_root = get(f"{self.base_url}{self.year}/drivers")
		ret_val = etree.fromstring(drivers_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def driver_information(self, driver_id):
		drivers_root = get(f"{self.base_url}drivers/{driver_id}")
		ret_val = etree.fromstring(drivers_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# Constructors
	def constructors_for_year(self):
		# There isn't much point in this? No team has ever pulled out halfway through a season?
		if self.race_number:
			constructors_root = get(f"{self.base_url}{self.year}/{self.race_number}/constructors")
		else:
			constructors_root = get(f"{self.base_url}{self.year}/constructors")
		ret_val = etree.fromstring(constructors_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# Circuts
	def circuts_for_year(self):
		# This is a bit more useful as it dosent seem that the circuts are in race order, but alphabetical
		if self.race_number:
			circuts_root = get(f"{self.base_url}{self.year}/{self.race_number}/circuits")
		else:
			circuts_root = get(f"{self.base_url}{self.year}/circuits")
		# TODO: Special characters (e.g. ü) print in unicode, fix
		ret_val = etree.fromstring(circuts_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# result
	def results(self):
		# This is cool
		# Most recent race result: replace year and race_number with current and last
		if not self.race_number:
			return "You need to specify a race_number"
		results_root = get(f"{self.base_url}{self.year}/{self.race_number}/results")
		ret_val = etree.fromstring(results_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# Seasons
	# Ignore the type hint here
	def schedule_for_year(self):
		# This has date and time
		# Can do year = "current"
		schedule_root = get(f"{self.base_url}{self.year}")
		ret_val = etree.fromstring(schedule_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def season_list(self):
		schedule_root = get(f"{self.base_url}2021")
		ret_val = etree.fromstring(schedule_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# Qualifying
	def qualifying_results(self, year="current", race_number="last"):
		schedule_root = get(f"{self.base_url}{year}/{race_number}/qualifying")
		ret_val = etree.fromstring(schedule_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# Standings
	def driver_standings_after_a_race(self):
		# This has date and time
		if not self.race_number:
			drivers_standings_root = get(f"{self.base_url}{self.year}/driverStandings")
		else:
			drivers_standings_root = get(f"{self.base_url}{self.year}/{self.race_number}/driverStandings")
		ret_val = etree.fromstring(drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def constructor_standings_after_a_race(self):
		if not self.race_number:
			constructor_standings_root = get(f"{self.base_url}{self.year}/constructorStandings")
		# This has date and time
		else:
			constructor_standings_root = get(f"{self.base_url}{self.year}/{self.race_number}/constructorStandings")
		ret_val = etree.fromstring(constructor_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def current_drivers_standings(self):
		current_drivers_standings_root = get(f"{self.base_url}current/driverStandings")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def current_constructors_standings(self):
		current_drivers_standings_root = get(f"{self.base_url}current/constructorStandings")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def all_winners_of_drivers_championships(self):
		# TODO: starts at 1950, limit = datetime current year - 1950, can offset it too and can change finishing position
		current_drivers_standings_root = get(f"{self.base_url}driverStandings/1?limit=25&offset=45")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def all_winners_of_constructors_championships(self):
		# Can offset it too and can change limit
		current_drivers_standings_root = get(f"{self.base_url}constructorStandings/1")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def driver_standings_by_specifying_the_driver(self, driver_id):
		current_drivers_standings_root = get(f"{self.base_url}drivers/{driver_id}/driverStandings")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def constructor_standings_by_specifying_the_constructor(self, constructer_id):
		# Could limit 1 here to get first year team was in f1
		current_drivers_standings_root = get(f"{self.base_url}constructors/{constructer_id}/constructorStandings")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# Finishing status
	def list_of_all_finishing_status_codes(self):
		# There's 135 status codes here so far but just set to 150
		# Basically tells you how many times drivers have finished, been disqualified, injured etc.
		# Could merge with 2 methods below

		current_drivers_standings_root = get(f"{self.base_url}status?limit=150")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def list_of_finishing_status_for_a_specific_season(self):
		current_drivers_standings_root = get(f"{self.base_url}{self.year}/status")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def list_of_finishing_status_for_a_specific_race_number_in_a_season(self):
		current_drivers_standings_root = get(f"{self.base_url}{self.year}/{self.race_number}/status")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# Lap times
	def lap_times(self, lapnumber=None):
		# Maybe not the best idea to not specify lapnumber as returns > 1000 results
		# Leaving in for now
		get_url = f"{self.base_url}{self.year}/{self.race_number}/laps"

		if lapnumber:
			get_url += f"/{lapnumber}"

		current_drivers_standings_root = get(get_url)
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# Pit stops
	def pit_stop_data_for_a_race(self):
		current_drivers_standings_root = get(f"{self.base_url}{self.year}/{self.race_number}/pitstops")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def specific_pit_stop_data_for_a_race(self, pitstop_number):
		current_drivers_standings_root = get(f"{self.base_url}{self.year}/{self.race_number}/pitstops/{pitstop_number}")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	@staticmethod
	def main():
		api_call = APICalls(2021, 5)
		# Next: All winners of drivers' championships
		print(api_call.specific_pit_stop_data_for_a_race(1))


if __name__ == "__main__":
	api_call = APICalls()
	api_call.main()
