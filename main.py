from requests import get
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime


class APICalls:
	current_year = datetime.today().year

	def __init__(self, year=current_year, round=None):
		self.year = year
		self.round = round

	def drivers_for_year(self):
		drivers_root = get(f"http://ergast.com/api/f1/{self.year}/drivers")
		ret_val = etree.fromstring(drivers_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def constructors_for_year(self):
		# There isn't much point in this? No team has ever pulled out halfway through a season?
		if self.round:
			constructors_root = get(f"http://ergast.com/api/f1/{self.year}/{self.round}/constructors")
		else:
			constructors_root = get(f"http://ergast.com/api/f1/{self.year}/constructors")
		ret_val = etree.fromstring(constructors_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def circuts_for_year(self):
		# This is a bit more useful as it dosent seem that the circuts are in race order, but alphabetical
		if self.round:
			circuts_root = get(f"http://ergast.com/api/f1/{self.year}/{self.round}/circuits")
		else:
			circuts_root = get(f"http://ergast.com/api/f1/{self.year}/circuits")
		# TODO: Special characters (e.g. ü) print in unicode, fix
		ret_val = etree.fromstring(circuts_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def results(self):
		# This is cool
		if not self.round:
			return "You need to specify a round"
		results_root = get(f"http://ergast.com/api/f1/{self.year}/{self.round}/results")
		ret_val = etree.fromstring(results_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	# Ignore the type hint here
	def schedule_for_year(self):
		# This has date and time
		schedule_root = get(f"http://ergast.com/api/f1/{self.year}")
		ret_val = etree.fromstring(schedule_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def driver_standings_after_a_race(self):
		# This has date and time
		if not self.round:
			drivers_standings_root = get(f"http://ergast.com/api/f1/{self.year}/driverStandings")
		else:
			drivers_standings_root = get(f"http://ergast.com/api/f1/{self.year}/{self.round}/driverStandings")
		ret_val = etree.fromstring(drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def constructor_standings_after_a_race(self):
		if not self.round:
			constructor_standings_root = get(f"http://ergast.com/api/f1/{self.year}/constructorStandings")
		# This has date and time
		else:
			constructor_standings_root = get(f"http://ergast.com/api/f1/{self.year}/{self.round}/constructorStandings")
		ret_val = etree.fromstring(constructor_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def current_drivers_standings(self):
		current_drivers_standings_root = get("http://ergast.com/api/f1/current/driverStandings")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def current_constructors_standings(self):
		current_drivers_standings_root = get("http://ergast.com/api/f1/current/constructorStandings")
		ret_val = etree.fromstring(current_drivers_standings_root.content)
		return etree.tostring(ret_val, pretty_print=True).decode()

	def main(self):
		api_call = APICalls(2020, 14)
		# Next: All winners of drivers' championships
		print(api_call.current_constructors_standings())

if __name__ == "__main__":
	api_call = APICalls()
	api_call.main()