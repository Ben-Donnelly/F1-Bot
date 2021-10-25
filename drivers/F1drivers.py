from requests import get
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from re import match, I


class Drivers:
	current_year = datetime.today().year

	def __init__(self, driver, driver_id=None, year=current_year):
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
		site = r"https://www.pitpass.com/drivers/46/max-verstappen"
		data = requests.get(site)
		soup = BeautifulSoup(data.text, 'html.parser')

		stats_res = soup.find('div', {'class': 'driverstatisticsvalue'}).contents[1]
		driver_res = soup.find('div', {'class': 'driverdetailsvalue2'}).contents[1]

		driver_information = {'DOB:': None,
							  'Age:': None,
							  'Height(m):': None,
							  'Height(ft):': None,
							  'Weight:': None,
							  'Relationship:': None,
							  'Place of birth:': None,
							  'Currently living:': None,
							  'total seasons:': None,
							  'Total races': None,
							  'Total championships:': None,
							  'Total wins': None,
							  'Total pole positions:': None,
							  'Total fastest laps': None,
							  'Total points': None,
							  'Total wins(2020)': None,
							  'pole positions(2020):': None,
							  'fastest laps(2020)': None,
							  'points(2020)': None,
							  'Current position': None}
		stats_results_list = []
		driver_results_list = []

		for i in range(0, len(driver_res), 2):
			driver_results_list.append(driver_res.contents[i].strip())

		for i in range(0, len(stats_res), 2):
			stats_results_list.append(stats_res.contents[i].strip())
		driver_results_list.insert(3, f"{str((float(driver_results_list[2][:3])) * 3.281)[:3]}ft")

		combined_results_list = driver_results_list + stats_results_list
		driver_information.update(zip(driver_information, combined_results_list))

		for k, v in driver_information.items():
			print(k, v)

	def map_names_to_id(self):
		drivers_for_year_call = self.drivers_for_year(just_drivers_list=True)
		driver_names = drivers_for_year_call[0]
		parse_driver_ids = drivers_for_year_call[1]
		driver_id_dict = {}

		for index, value in enumerate(parse_driver_ids):
			driver_id_dict[driver_names[index]] = value['driverId']

		return driver_id_dict
