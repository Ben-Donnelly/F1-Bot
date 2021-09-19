from requests import get
import json
from datetime import datetime
from re import match, I


class Drivers:
	current_year = datetime.today().year

	def __init__(self, year=current_year, driver=None, driver_id=None):
		self.year = year
		self.driver = driver
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.driver_id = driver_id
		self.return_values = {}

	def drivers_for_year(self, just_drivers_list=False):
		self.def_return_value = get(f"{self.base_url}/{self.year}/drivers.json")

		data = json.loads(self.def_return_value.text)
		drivers_list = data['MRData']['DriverTable']['Drivers']
		driver_full_name = [f"{driver['givenName']} {driver['familyName']}" for driver in drivers_list]

		if just_drivers_list:
			return driver_full_name, drivers_list

		has_data = self.def_return_value.raw._fp_bytes_read
		self.return_values = {"has_data": has_data,
							  "status_code": self.def_return_value.status_code,
							  "drivers": driver_full_name}

		# There are few ways of telling if there will be actual data here
		# If there is, _fp_bytes_read will be considerably higher than 500
		try:
			self.year = int(self.year)
		except ValueError:
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
		data = get(f'https://ergast.com/api/f1/2021/drivers/{self.driver_id}/driverStandings.json')
		self.def_return_value = json.loads(data.text)
		self.def_return_value = self.def_return_value['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

		# This check is not really needed now, but good for security I suppose
		# May take out later
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

		dob_for_age = datetime.fromisoformat(driver_dob).strftime("%B %d %Y")
		age = datetime.today().year - int(dob_for_age[-4:])

		print(f"{driver_first_name} {driver_last_name} is a {driver_nationality} driver\n"
				f"He is {age} years old, born on {dob_for_age}\n"
				f"{driver_number} is his driver number\n"
				f"He is currently P{driver_current_position} in the championship with {driver_current_points} points"
				f" and {driver_num_of_wins} wins this season\n"
				f"He races for the {constructor_nationality} team {constructor_name}")

		return self.return_values

	def map_names_to_id(self):
		drivers_for_year_call = self.drivers_for_year(just_drivers_list=True)
		driver_names = drivers_for_year_call[0]
		parse_driver_ids = drivers_for_year_call[1]
		driver_id_dict = {}

		for index, value in enumerate(parse_driver_ids):
			driver_id_dict[driver_names[index]] = value['driverId']

		return driver_id_dict
