from requests import get
import json
from re import match, I
from datetime import datetime
from drivers import F1drivers


class Results:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None, driver=None):
		self.year = year
		self.driver = driver
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""

	def results(self, compare_driver1=None, compare_driver2=None, circuit=None, compare_flag=False):
		if compare_flag:
			if not circuit:
				raise Exception('You need to specify a circuit')

			driver_call = F1drivers.Drivers()
			driver_id_dict = driver_call.map_names_to_id()

			d1_flag = False
			d2_flag = False
			compare_driver1_id = None
			compare_driver2_id = None

			for entry in driver_id_dict.keys():
				if not d1_flag and match(f".*{compare_driver1}.*", entry, flags=I):
					compare_driver1_id = driver_id_dict[entry]
					d1_flag = True

					self.driver_full_name = entry

				if not d2_flag and match(f".*{compare_driver2}.*", entry, flags=I):
					compare_driver2_id = driver_id_dict[entry]
					d2_flag = True

					# self.driver_full_name = entry

				if d1_flag and d2_flag:
					break

			if not compare_driver1_id or not compare_driver2_id:
				# TODO: display error message, test this
				quit()

			driver1_data = get(f"{self.base_url}/{self.year}/drivers/{compare_driver1_id}/circuits/{circuit}/results.json")
			driver2_data = get(f"{self.base_url}/{self.year}/drivers/{compare_driver2_id}/circuits/{circuit}/results.json")

			if driver1_data.status_code != 200 or driver2_data.status_code != 200:
				raise Exception('I could not find any data for the specified drivers and/or race')

			driver1_data = json.loads(driver1_data.text)
			driver2_data = json.loads(driver2_data.text)

			driver1_data = driver1_data['MRData']['RaceTable']['Races'][0]['Results'][0]
			driver2_data = driver2_data['MRData']['RaceTable']['Races'][0]['Results'][0]
			return {compare_driver1: driver1_data, compare_driver2: driver2_data}

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
