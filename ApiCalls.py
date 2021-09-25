from requests import get
import xml.etree.ElementTree as ET
from re import match, I
from bs4 import BeautifulSoup
from datetime import datetime
import json

class Call:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number="last", driver=None, driver_id=None, constructor_id=None, lapnumber=None, pitstop_number=None):
		self.year = year
		self.driver = driver
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.driver_id = driver_id
		self.constructor_id = constructor_id
		self.lapnumber = lapnumber
		self.pitstop_number = pitstop_number
		self.parser = None
		self.return_values = {}

	def validate_parameters(self):
		if self.race_number == 'last':
			self.extra_information = f"You did not specify a race number, so I got the information for the last race\n"

	def error_message(self):
		print(self.message)
		exit()

	# Drivers
	def drivers_for_year(self, justDriversList=False):
		self.def_return_value = get(f"{self.base_url}/{self.year}/drivers")
		self.parser = BeautifulSoup(self.def_return_value.text, "xml")

		driver_first_name = self.parser.find_all("GivenName")
		driver_last_name = self.parser.find_all('FamilyName')
		driver_full_name = [f"{fn.text} {ln.text}" for fn, ln in zip(driver_first_name, driver_last_name)]

		if justDriversList:
			driver_list = self.parser.find_all("Driver")
			return driver_full_name, driver_list

		has_data = self.def_return_value.raw._fp_bytes_read
		self.return_values = {"has_data": has_data, "status_code": self.def_return_value.status_code,
							  "drivers": driver_full_name}

		# There are few ways of telling if there will be actual data here
		# If there is, _fp_bytes_read will be considerably higher than 500
		try:
			self.year = int(self.year)
		except(ValueError):
			print(f"{self.year} is not a valid year")
			raise ValueError

		correct_verb = "were" if self.year < datetime.today().year else "are"
		if has_data > 500:
			print(f"Drivers racing for the {self.year} season {correct_verb}:\n")
			print(*driver_full_name, sep='\n')
			return self.return_values

		print(f"I do not have the data for the {self.year} season yet, sorry 😪")
		return self.return_values

	def driver_information(self):
		get_ids = self.map_names_to_id()

		if self.driver:
			self.driver = self.driver.title()
			for entry in get_ids.keys():
				if match(f".*{self.driver}.*", entry, flags=I):
					self.driver_id = get_ids[entry]
					self.driver_full_name = entry
					break

		if not self.driver_id:
			raise Exception('You need to specify a driver or driver id\n you can give me a full name, last name or id')

		# self.def_return_value = get(f"{self.base_url}/drivers/{self.driver_id}")
		data = get('https://ergast.com/api/f1/2021/driverstandings.json')
		self.def_return_value = json.loads(data.text)
		self.def_return_value = self.def_return_value['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

		required_driver_details = {}
		for i in self.def_return_value:
			if i['Driver']['driverId'] == self.driver_id:
				required_driver_details = i
				break
		# self.parser = BeautifulSoup(self.def_return_value.text, "xml")
		# Todo: if name, e.g misspelled, not a driver etc. print that here (check length like in has_data above
		# Todo: tests
		driver_current_position = required_driver_details['position']
		driver_current_points = required_driver_details['points']
		driver_num_of_wins = required_driver_details['wins']

		required_driver_constructor = required_driver_details['Constructors'][0]
		constructor_nationality = required_driver_constructor['nationality']
		constructor_name = required_driver_constructor['name']

		required_driver_details = required_driver_details['Driver']
		driver_first_name = required_driver_details['givenName']
		driver_last_name = required_driver_details['familyName']
		driver_number = required_driver_details['permanentNumber']
		driver_dob = required_driver_details['dateOfBirth']
		driver_nationality = required_driver_details['nationality']

		# driver_number = self.parser.find("PermanentNumber").text
		# driver_dob = datetime.fromisoformat(driver_dob)
		dob_for_age = datetime.fromisoformat(driver_dob).strftime("%B %d %Y")
		age = datetime.today().year - int(dob_for_age[-4:])

		print(f"{driver_first_name} {driver_last_name} is a {driver_nationality} driver\n"
			  f"He is {age} years old, born on {dob_for_age}\n"
			  f"{driver_number} is his driver number\n"
			  f"He is currently P{driver_current_position} in the championship with {driver_current_points} points"
			  f" and {driver_num_of_wins} wins this season\n"
			  f"He races for the {constructor_nationality} team {constructor_name}")
		# has_data = self.def_return_value.raw._fp_bytes_read
		# self.return_values = {"has_data": has_data, "status_code": self.def_return_value.status_code,
		# 					  "has_id": self.driver_id != None}
		return self.return_values

	# Constructors
	def constructors_for_year(self):
		# There isn't much point in this? No team has ever pulled out halfway through a season?
		if self.race_number:
			self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/constructors")
		else:
			self.def_return_value = get(f"{self.base_url}/{self.year}/constructors")
		self.validate_parameters()
		print(self.def_return_value.text)
		"""
		<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="/schemas/mrd-1.4.xsl"?>
<MRData xmlns="http://ergast.com/mrd/1.4" series="f1" url="http://ergast.com/api/f1/2021/last/constructors" limit="30" offset="0" total="10">
	<ConstructorTable season="2021" round="14">
		<Constructor constructorId="alfa" url="http://en.wikipedia.org/wiki/Alfa_Romeo_in_Formula_One">
			<Name>Alfa Romeo</Name>
			<Nationality>Swiss</Nationality>
		</Constructor>
		<Constructor constructorId="alphatauri" url="http://en.wikipedia.org/wiki/Scuderia_AlphaTauri">
			<Name>AlphaTauri</Name>
			<Nationality>Italian</Nationality>
		</Constructor>
		<Constructor constructorId="alpine" url="http://en.wikipedia.org/wiki/Alpine_F1_Team">
			<Name>Alpine F1 Team</Name>
			<Nationality>French</Nationality>
		</Constructor>
		<Constructor constructorId="aston_martin" url="http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One">
			<Name>Aston Martin</Name>
			<Nationality>British</Nationality>
		</Constructor>
		<Constructor constructorId="ferrari" url="http://en.wikipedia.org/wiki/Scuderia_Ferrari">
			<Name>Ferrari</Name>
			<Nationality>Italian</Nationality>
		</Constructor>
		<Constructor constructorId="haas" url="http://en.wikipedia.org/wiki/Haas_F1_Team">
			<Name>Haas F1 Team</Name>
			<Nationality>American</Nationality>
		</Constructor>
		<Constructor constructorId="mclaren" url="http://en.wikipedia.org/wiki/McLaren">
			<Name>McLaren</Name>
			<Nationality>British</Nationality>
		</Constructor>
		<Constructor constructorId="mercedes" url="http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One">
			<Name>Mercedes</Name>
			<Nationality>German</Nationality>
		</Constructor>
		<Constructor constructorId="red_bull" url="http://en.wikipedia.org/wiki/Red_Bull_Racing">
			<Name>Red Bull</Name>
			<Nationality>Austrian</Nationality>
		</Constructor>
		<Constructor constructorId="williams" url="http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering">
			<Name>Williams</Name>
			<Nationality>British</Nationality>
		</Constructor>
	</ConstructorTable>
</MRData>

		"""

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
	def lap_times(self):
		# Maybe not the best idea to not specify lapnumber as returns > 1000 results
		# Leaving in for now
		get_url = f"{self.base_url}/{self.year}/{self.race_number}/laps"
		if self.lapnumber:
			get_url += f"/{self.lapnumber}"

		self.def_return_value = get(get_url)
		self.validate_parameters()
		return self

	# Pit stops
	def pit_stop_data_for_a_race(self):
		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/pitstops")
		self.validate_parameters()
		return self

	def specific_pit_stop_data_for_a_race(self):
		if not self.pitstop_number:
			self.message = "You need to specify a constructor id"
			return self.error_message()

		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/pitstops/{self.pitstop_number}")
		self.validate_parameters()
		return self

	def map_names_to_id(self):
		drivers_for_year_call = self.drivers_for_year(justDriversList=True)
		driver_names = drivers_for_year_call[0]
		parse_driver_ids = drivers_for_year_call[1]
		driver_id_dict = {}

		for index, value in enumerate(parse_driver_ids):
			driver_id_dict[driver_names[index]] = value.attrs['driverId']

		return driver_id_dict

	# def map_driver_to_team(self):
	# 	driver_standings_call = self.driver_standings_after_a_race()
	# 	print(driver_standings_call)


	@staticmethod
	def to_string(data):
		return data
		# to_string_return_value = ET.fromstring(data.def_return_value.content)
		# return f"{data.extra_information}{ET.tostring(to_string_return_value, pretty_print=True).decode()}"

	@staticmethod
	def main():
		# noinspection PyTypeChecker
		api_call = Call(driver="yuki tsunoda")

		# api_call_result = api_call.drivers_for_year()
		# bs = etree.XML(api_call_result.def_return_value.content)
		# etree.indent(bs)
		# print(etree.tostring(bs, encoding='unicode'))

		api_call_result = api_call.driver_information()
		x = api_call_result

		# print(api_call_result.def_return_value.content)
		# root = ET.fromstring(api_call_result.def_return_value.text)
		# print(root.findall("[tag='Driver']"))

		# bs = etree.parse(api_call_result.def_return_value.content)
		# print(type(bs))
		# print(bs.getroot())

		# print(api_call.to_string(api_call_result))


if __name__ == "__main__":
	call = Call()
	call.main()
