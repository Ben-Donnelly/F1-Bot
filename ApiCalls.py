from requests import get
import xml.etree.ElementTree as ET
from re import match, I
from bs4 import BeautifulSoup
from datetime import datetime
import json

class Call:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None, driver=None, driver_id=None, constructor_id=None, lapnumber=None, pitstop_number=None):
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
		self.def_return_value = get(f"{self.base_url}/{self.year}/drivers.json")

		data = json.loads(self.def_return_value.text)
		drivers_list = data['MRData']['DriverTable']['Drivers']
		driver_full_name = [f"{driver['givenName']} {driver['familyName']}" for driver in drivers_list]

		if justDriversList:
			return driver_full_name, drivers_list

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
		# has_data = self.def_return_value.raw._fp_bytes_read
		# self.return_values = {"has_data": has_data, "status_code": self.def_return_value.status_code,
		# 					  "has_id": self.driver_id != None}
		return self.return_values

	# Constructors
	def constructors_for_year(self):
		# There isn't much point in this? No team has ever pulled out halfway through a season?
		if self.race_number:
			data = get(f"{self.base_url}/{self.year}/{self.race_number}/constructors.json")
		else:
			data = get(f"{self.base_url}/{self.year}/constructors.json")

		data = json.loads(data.text)
		constructors_list = data['MRData']['ConstructorTable']['Constructors']
		for i in constructors_list:
			print(f"{i['name']} ({i['nationality']})")


	# Circuts
	def circuts_for_year(self):
		if self.race_number:
			data = get(f"{self.base_url}/{self.year}/{self.race_number}.json")
		else:
			data = get(f"{self.base_url}/{self.year}.json")
		self.validate_parameters()

		data = json.loads(data.text)
		races_list = data['MRData']['RaceTable']['Races']
		for race in races_list:
			print(f"Race {race['round']}: {race['raceName']} ({race['Circuit']['circuitName']}, {race['Circuit']['Location']['locality']}, {race['Circuit']['Location']['country']}, {race['date']}, {race['time']})")
		# print(circuts_list)
		quit()

		# TODO: Special characters (e.g. ü) print in unicode, fix
		return self

	# result
	def results(self):
		# Here Next
		# This is cool
		# Most recent race result: replace year and race_number with current and last
		# if not self.race_number:
		# 	self.race_number = 'last'
		# if not self.year:
		# 	self.year = 'current'
		# data = get(f"{self.base_url}/{self.year}/{self.race_number}/results.json")
		# self.validate_parameters()
		print(f"{self.base_url}/{self.year}/{self.race_number}/results.json")
		# data = json.loads(data.text)
		data = """{
 "MRData": {
  "RaceTable": {
   "Races": [
    {
     "Circuit": {
      "Location": {
       "country": "Russia",
       "lat": "43.4057",
       "locality": "Sochi",
       "long": "39.9578"
      },
      "circuitId": "sochi",
      "circuitName": "Sochi Autodrom",
      "url": "http://en.wikipedia.org/wiki/Sochi_Autodrom"
     },
     "Results": [
      {
       "Constructor": {
        "constructorId": "mercedes",
        "name": "Mercedes",
        "nationality": "German",
        "url": "http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One"
       },
       "Driver": {
        "code": "HAM",
        "dateOfBirth": "1985-01-07",
        "driverId": "hamilton",
        "familyName": "Hamilton",
        "givenName": "Lewis",
        "nationality": "British",
        "permanentNumber": "44",
        "url": "http://en.wikipedia.org/wiki/Lewis_Hamilton"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "215.760",
         "units": "kph"
        },
        "Time": {
         "time": "1:37.575"
        },
        "lap": "43",
        "rank": "2"
       },
       "Time": {
        "millis": "5441001",
        "time": "1:30:41.001"
       },
       "grid": "4",
       "laps": "53",
       "number": "44",
       "points": "25",
       "position": "1",
       "positionText": "1",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "red_bull",
        "name": "Red Bull",
        "nationality": "Austrian",
        "url": "http://en.wikipedia.org/wiki/Red_Bull_Racing"
       },
       "Driver": {
        "code": "VER",
        "dateOfBirth": "1997-09-30",
        "driverId": "max_verstappen",
        "familyName": "Verstappen",
        "givenName": "Max",
        "nationality": "Dutch",
        "permanentNumber": "33",
        "url": "http://en.wikipedia.org/wiki/Max_Verstappen"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "213.959",
         "units": "kph"
        },
        "Time": {
         "time": "1:38.396"
        },
        "lap": "28",
        "rank": "5"
       },
       "Time": {
        "millis": "5494272",
        "time": "+53.271"
       },
       "grid": "20",
       "laps": "53",
       "number": "33",
       "points": "18",
       "position": "2",
       "positionText": "2",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "ferrari",
        "name": "Ferrari",
        "nationality": "Italian",
        "url": "http://en.wikipedia.org/wiki/Scuderia_Ferrari"
       },
       "Driver": {
        "code": "SAI",
        "dateOfBirth": "1994-09-01",
        "driverId": "sainz",
        "familyName": "Sainz",
        "givenName": "Carlos",
        "nationality": "Spanish",
        "permanentNumber": "55",
        "url": "http://en.wikipedia.org/wiki/Carlos_Sainz_Jr."
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "212.024",
         "units": "kph"
        },
        "Time": {
         "time": "1:39.294"
        },
        "lap": "40",
        "rank": "12"
       },
       "Time": {
        "millis": "5503476",
        "time": "+1:02.475"
       },
       "grid": "2",
       "laps": "53",
       "number": "55",
       "points": "15",
       "position": "3",
       "positionText": "3",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "mclaren",
        "name": "McLaren",
        "nationality": "British",
        "url": "http://en.wikipedia.org/wiki/McLaren"
       },
       "Driver": {
        "code": "RIC",
        "dateOfBirth": "1989-07-01",
        "driverId": "ricciardo",
        "familyName": "Ricciardo",
        "givenName": "Daniel",
        "nationality": "Australian",
        "permanentNumber": "3",
        "url": "http://en.wikipedia.org/wiki/Daniel_Ricciardo"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "212.388",
         "units": "kph"
        },
        "Time": {
         "time": "1:39.124"
        },
        "lap": "24",
        "rank": "9"
       },
       "Time": {
        "millis": "5506608",
        "time": "+1:05.607"
       },
       "grid": "5",
       "laps": "53",
       "number": "3",
       "points": "12",
       "position": "4",
       "positionText": "4",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "mercedes",
        "name": "Mercedes",
        "nationality": "German",
        "url": "http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One"
       },
       "Driver": {
        "code": "BOT",
        "dateOfBirth": "1989-08-28",
        "driverId": "bottas",
        "familyName": "Bottas",
        "givenName": "Valtteri",
        "nationality": "Finnish",
        "permanentNumber": "77",
        "url": "http://en.wikipedia.org/wiki/Valtteri_Bottas"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "214.352",
         "units": "kph"
        },
        "Time": {
         "time": "1:38.216"
        },
        "lap": "31",
        "rank": "3"
       },
       "Time": {
        "millis": "5508534",
        "time": "+1:07.533"
       },
       "grid": "16",
       "laps": "53",
       "number": "77",
       "points": "10",
       "position": "5",
       "positionText": "5",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "alpine",
        "name": "Alpine F1 Team",
        "nationality": "French",
        "url": "http://en.wikipedia.org/wiki/Alpine_F1_Team"
       },
       "Driver": {
        "code": "ALO",
        "dateOfBirth": "1981-07-29",
        "driverId": "alonso",
        "familyName": "Alonso",
        "givenName": "Fernando",
        "nationality": "Spanish",
        "permanentNumber": "14",
        "url": "http://en.wikipedia.org/wiki/Fernando_Alonso"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "213.331",
         "units": "kph"
        },
        "Time": {
         "time": "1:38.686"
        },
        "lap": "44",
        "rank": "6"
       },
       "Time": {
        "millis": "5522322",
        "time": "+1:21.321"
       },
       "grid": "6",
       "laps": "53",
       "number": "14",
       "points": "8",
       "position": "6",
       "positionText": "6",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "mclaren",
        "name": "McLaren",
        "nationality": "British",
        "url": "http://en.wikipedia.org/wiki/McLaren"
       },
       "Driver": {
        "code": "NOR",
        "dateOfBirth": "1999-11-13",
        "driverId": "norris",
        "familyName": "Norris",
        "givenName": "Lando",
        "nationality": "British",
        "permanentNumber": "4",
        "url": "http://en.wikipedia.org/wiki/Lando_Norris"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "216.096",
         "units": "kph"
        },
        "Time": {
         "time": "1:37.423"
        },
        "lap": "39",
        "rank": "1"
       },
       "Time": {
        "millis": "5528225",
        "time": "+1:27.224"
       },
       "grid": "1",
       "laps": "53",
       "number": "4",
       "points": "7",
       "position": "7",
       "positionText": "7",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "alfa",
        "name": "Alfa Romeo",
        "nationality": "Swiss",
        "url": "http://en.wikipedia.org/wiki/Alfa_Romeo_in_Formula_One"
       },
       "Driver": {
        "code": "RAI",
        "dateOfBirth": "1979-10-17",
        "driverId": "raikkonen",
        "familyName": "R\u00e4ikk\u00f6nen",
        "givenName": "Kimi",
        "nationality": "Finnish",
        "permanentNumber": "7",
        "url": "http://en.wikipedia.org/wiki/Kimi_R%C3%A4ikk%C3%B6nen"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "209.921",
         "units": "kph"
        },
        "Time": {
         "time": "1:40.289"
        },
        "lap": "34",
        "rank": "16"
       },
       "Time": {
        "millis": "5529956",
        "time": "+1:28.955"
       },
       "grid": "13",
       "laps": "53",
       "number": "7",
       "points": "4",
       "position": "8",
       "positionText": "8",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "red_bull",
        "name": "Red Bull",
        "nationality": "Austrian",
        "url": "http://en.wikipedia.org/wiki/Red_Bull_Racing"
       },
       "Driver": {
        "code": "PER",
        "dateOfBirth": "1990-01-26",
        "driverId": "perez",
        "familyName": "P\u00e9rez",
        "givenName": "Sergio",
        "nationality": "Mexican",
        "permanentNumber": "11",
        "url": "http://en.wikipedia.org/wiki/Sergio_P%C3%A9rez"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "212.193",
         "units": "kph"
        },
        "Time": {
         "time": "1:39.215"
        },
        "lap": "45",
        "rank": "10"
       },
       "Time": {
        "millis": "5531077",
        "time": "+1:30.076"
       },
       "grid": "8",
       "laps": "53",
       "number": "11",
       "points": "2",
       "position": "9",
       "positionText": "9",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "williams",
        "name": "Williams",
        "nationality": "British",
        "url": "http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering"
       },
       "Driver": {
        "code": "RUS",
        "dateOfBirth": "1998-02-15",
        "driverId": "russell",
        "familyName": "Russell",
        "givenName": "George",
        "nationality": "British",
        "permanentNumber": "63",
        "url": "http://en.wikipedia.org/wiki/George_Russell_%28racing_driver%29"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "209.280",
         "units": "kph"
        },
        "Time": {
         "time": "1:40.596"
        },
        "lap": "40",
        "rank": "18"
       },
       "Time": {
        "millis": "5541552",
        "time": "+1:40.551"
       },
       "grid": "3",
       "laps": "53",
       "number": "63",
       "points": "1",
       "position": "10",
       "positionText": "10",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "aston_martin",
        "name": "Aston Martin",
        "nationality": "British",
        "url": "http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One"
       },
       "Driver": {
        "code": "STR",
        "dateOfBirth": "1998-10-29",
        "driverId": "stroll",
        "familyName": "Stroll",
        "givenName": "Lance",
        "nationality": "Canadian",
        "permanentNumber": "18",
        "url": "http://en.wikipedia.org/wiki/Lance_Stroll"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "209.555",
         "units": "kph"
        },
        "Time": {
         "time": "1:40.464"
        },
        "lap": "35",
        "rank": "17"
       },
       "Time": {
        "millis": "5547199",
        "time": "+1:46.198"
       },
       "grid": "7",
       "laps": "53",
       "number": "18",
       "points": "0",
       "position": "11",
       "positionText": "11",
       "status": "Finished"
      },
      {
       "Constructor": {
        "constructorId": "aston_martin",
        "name": "Aston Martin",
        "nationality": "British",
        "url": "http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One"
       },
       "Driver": {
        "code": "VET",
        "dateOfBirth": "1987-07-03",
        "driverId": "vettel",
        "familyName": "Vettel",
        "givenName": "Sebastian",
        "nationality": "German",
        "permanentNumber": "5",
        "url": "http://en.wikipedia.org/wiki/Sebastian_Vettel"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "212.116",
         "units": "kph"
        },
        "Time": {
         "time": "1:39.251"
        },
        "lap": "44",
        "rank": "11"
       },
       "grid": "10",
       "laps": "52",
       "number": "5",
       "points": "0",
       "position": "12",
       "positionText": "12",
       "status": "+1 Lap"
      },
      {
       "Constructor": {
        "constructorId": "alphatauri",
        "name": "AlphaTauri",
        "nationality": "Italian",
        "url": "http://en.wikipedia.org/wiki/Scuderia_AlphaTauri"
       },
       "Driver": {
        "code": "GAS",
        "dateOfBirth": "1996-02-07",
        "driverId": "gasly",
        "familyName": "Gasly",
        "givenName": "Pierre",
        "nationality": "French",
        "permanentNumber": "10",
        "url": "http://en.wikipedia.org/wiki/Pierre_Gasly"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "214.214",
         "units": "kph"
        },
        "Time": {
         "time": "1:38.279"
        },
        "lap": "35",
        "rank": "4"
       },
       "grid": "11",
       "laps": "52",
       "number": "10",
       "points": "0",
       "position": "13",
       "positionText": "13",
       "status": "+1 Lap"
      },
      {
       "Constructor": {
        "constructorId": "alpine",
        "name": "Alpine F1 Team",
        "nationality": "French",
        "url": "http://en.wikipedia.org/wiki/Alpine_F1_Team"
       },
       "Driver": {
        "code": "OCO",
        "dateOfBirth": "1996-09-17",
        "driverId": "ocon",
        "familyName": "Ocon",
        "givenName": "Esteban",
        "nationality": "French",
        "permanentNumber": "31",
        "url": "http://en.wikipedia.org/wiki/Esteban_Ocon"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "209.276",
         "units": "kph"
        },
        "Time": {
         "time": "1:40.598"
        },
        "lap": "34",
        "rank": "19"
       },
       "grid": "9",
       "laps": "52",
       "number": "31",
       "points": "0",
       "position": "14",
       "positionText": "14",
       "status": "+1 Lap"
      },
      {
       "Constructor": {
        "constructorId": "ferrari",
        "name": "Ferrari",
        "nationality": "Italian",
        "url": "http://en.wikipedia.org/wiki/Scuderia_Ferrari"
       },
       "Driver": {
        "code": "LEC",
        "dateOfBirth": "1997-10-16",
        "driverId": "leclerc",
        "familyName": "Leclerc",
        "givenName": "Charles",
        "nationality": "Monegasque",
        "permanentNumber": "16",
        "url": "http://en.wikipedia.org/wiki/Charles_Leclerc"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "212.667",
         "units": "kph"
        },
        "Time": {
         "time": "1:38.994"
        },
        "lap": "45",
        "rank": "7"
       },
       "grid": "19",
       "laps": "52",
       "number": "16",
       "points": "0",
       "position": "15",
       "positionText": "15",
       "status": "+1 Lap"
      },
      {
       "Constructor": {
        "constructorId": "alfa",
        "name": "Alfa Romeo",
        "nationality": "Swiss",
        "url": "http://en.wikipedia.org/wiki/Alfa_Romeo_in_Formula_One"
       },
       "Driver": {
        "code": "GIO",
        "dateOfBirth": "1993-12-14",
        "driverId": "giovinazzi",
        "familyName": "Giovinazzi",
        "givenName": "Antonio",
        "nationality": "Italian",
        "permanentNumber": "99",
        "url": "http://en.wikipedia.org/wiki/Antonio_Giovinazzi"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "212.530",
         "units": "kph"
        },
        "Time": {
         "time": "1:39.058"
        },
        "lap": "39",
        "rank": "8"
       },
       "grid": "17",
       "laps": "52",
       "number": "99",
       "points": "0",
       "position": "16",
       "positionText": "16",
       "status": "+1 Lap"
      },
      {
       "Constructor": {
        "constructorId": "alphatauri",
        "name": "AlphaTauri",
        "nationality": "Italian",
        "url": "http://en.wikipedia.org/wiki/Scuderia_AlphaTauri"
       },
       "Driver": {
        "code": "TSU",
        "dateOfBirth": "2000-05-11",
        "driverId": "tsunoda",
        "familyName": "Tsunoda",
        "givenName": "Yuki",
        "nationality": "Japanese",
        "permanentNumber": "22",
        "url": "http://en.wikipedia.org/wiki/Yuki_Tsunoda"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "210.612",
         "units": "kph"
        },
        "Time": {
         "time": "1:39.960"
        },
        "lap": "42",
        "rank": "13"
       },
       "grid": "12",
       "laps": "52",
       "number": "22",
       "points": "0",
       "position": "17",
       "positionText": "17",
       "status": "+1 Lap"
      },
      {
       "Constructor": {
        "constructorId": "haas",
        "name": "Haas F1 Team",
        "nationality": "American",
        "url": "http://en.wikipedia.org/wiki/Haas_F1_Team"
       },
       "Driver": {
        "code": "MAZ",
        "dateOfBirth": "1999-03-02",
        "driverId": "mazepin",
        "familyName": "Mazepin",
        "givenName": "Nikita",
        "nationality": "Russian",
        "permanentNumber": "9",
        "url": "http://en.wikipedia.org/wiki/Nikita_Mazepin"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "206.982",
         "units": "kph"
        },
        "Time": {
         "time": "1:41.713"
        },
        "lap": "24",
        "rank": "20"
       },
       "grid": "15",
       "laps": "51",
       "number": "9",
       "points": "0",
       "position": "18",
       "positionText": "18",
       "status": "+2 Laps"
      },
      {
       "Constructor": {
        "constructorId": "williams",
        "name": "Williams",
        "nationality": "British",
        "url": "http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering"
       },
       "Driver": {
        "code": "LAT",
        "dateOfBirth": "1995-06-29",
        "driverId": "latifi",
        "familyName": "Latifi",
        "givenName": "Nicholas",
        "nationality": "Canadian",
        "permanentNumber": "6",
        "url": "http://en.wikipedia.org/wiki/Nicholas_Latifi"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "210.528",
         "units": "kph"
        },
        "Time": {
         "time": "1:40.000"
        },
        "lap": "42",
        "rank": "14"
       },
       "grid": "18",
       "laps": "47",
       "number": "6",
       "points": "0",
       "position": "19",
       "positionText": "19",
       "status": "Accident"
      },
      {
       "Constructor": {
        "constructorId": "haas",
        "name": "Haas F1 Team",
        "nationality": "American",
        "url": "http://en.wikipedia.org/wiki/Haas_F1_Team"
       },
       "Driver": {
        "code": "MSC",
        "dateOfBirth": "1999-03-22",
        "driverId": "mick_schumacher",
        "familyName": "Schumacher",
        "givenName": "Mick",
        "nationality": "German",
        "permanentNumber": "47",
        "url": "http://en.wikipedia.org/wiki/Mick_Schumacher"
       },
       "FastestLap": {
        "AverageSpeed": {
         "speed": "209.948",
         "units": "kph"
        },
        "Time": {
         "time": "1:40.276"
        },
        "lap": "22",
        "rank": "15"
       },
       "grid": "14",
       "laps": "32",
       "number": "47",
       "points": "0",
       "position": "20",
       "positionText": "R",
       "status": "Oil leak"
      }
     ],
     "date": "2021-09-26",
     "raceName": "Russian Grand Prix",
     "round": "15",
     "season": "2021",
     "time": "12:00:00Z",
     "url": "http://en.wikipedia.org/wiki/2021_Russian_Grand_Prix"
    }
   ],
   "round": "15",
   "season": "2021"
  },
  "limit": "30",
  "offset": "0",
  "series": "f1",
  "total": "20",
  "url": "http://ergast.com/api/f1/2021/last/results.json",
  "xmlns": "http://ergast.com/mrd/1.4"
 }
}

"""
		data = json.loads(data)

		data = data['MRData']['RaceTable']['Races'][0]
		# print(data)
		# quit()
		for i in data['Results']:
			print(i)
			# print()
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
		if not self.race_number:
			self.race_number = 'last'

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
		if not self.race_number:
			self.race_number = 'last'

		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/status")
		self.validate_parameters()
		return self

	# Lap times
	def lap_times(self):
		# Maybe not the best idea to not specify lapnumber as returns > 1000 results
		# Leaving in for now
		if not self.race_number:
			self.race_number = 'last'

		get_url = f"{self.base_url}/{self.year}/{self.race_number}/laps"
		if self.lapnumber:
			get_url += f"/{self.lapnumber}"

		self.def_return_value = get(get_url)
		self.validate_parameters()
		return self

	# Pit stops
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

		self.def_return_value = get(f"{self.base_url}/{self.year}/{self.race_number}/pitstops/{self.pitstop_number}")
		self.validate_parameters()
		return self

	def map_names_to_id(self):
		drivers_for_year_call = self.drivers_for_year(justDriversList=True)
		driver_names = drivers_for_year_call[0]
		parse_driver_ids = drivers_for_year_call[1]
		driver_id_dict = {}

		for index, value in enumerate(parse_driver_ids):
			driver_id_dict[driver_names[index]] = value['driverId']

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
		api_call = Call(driver="Lewis hamilton")

		# api_call_result = api_call.drivers_for_year()
		# bs = etree.XML(api_call_result.def_return_value.content)
		# etree.indent(bs)
		# print(etree.tostring(bs, encoding='unicode'))

		api_call_result = api_call.results()
		# print(api_call_result)

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
