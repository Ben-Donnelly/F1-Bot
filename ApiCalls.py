from requests import get
import xml.etree.ElementTree as ET
from re import match, I
from bs4 import BeautifulSoup
from datetime import datetime
import json

class Call:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None):

		self.year = year
		self.driver = driver
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}

	def validate_parameters(self):
		if self.race_number == 'last':
			self.extra_information = f"You did not specify a race number, so I got the information for the last race\n"

	def error_message(self):
		print(self.message)
		exit()

	def compare_2_drivers_from_a_race(self, driver1, driver2, circut=None):
		if not driver1 and driver2:
			raise Exception('You need to specify 2 drivers to compare')

		if not circut:
			raise Exception('You need to specify a circut')

		data = self.results(compareDriver1=driver1, compareDriver2=driver2, circut=circut, compare_flag=True)
		d1, d2 = data.keys()

		# Next: Here
		# Note: This is broken both times are equal
		# Dont blame me for the bad code here, I'm tired and I will fix it
		d1_fastest_lap = data[d1]['FastestLap']['Time']['time']
		d2_fastest_lap = data[d2]['FastestLap']['Time']['time']

		format = '%M:%S.%f'
		d_fastest_time = (datetime.strptime(d1_fastest_lap, format) - datetime.strptime(d2_fastest_lap, format)).total_seconds()

		if d_fastest_time > 0:
			data['driver_with_fastest_lap'] = d1
			data['driver_with_fastest_lap_time'] = d1_fastest_lap
			data['driver_with_2nd_fastest_lap'] = d2
			data['driver_with_2nd_fastest_lap_time'] = d2_fastest_lap
		else:
			data['driver_with_fastest_lap'] = d2
			data['driver_with_fastest_lap_time'] = d2_fastest_lap
			data['driver_with_2nd_fastest_lap'] = d1
			data['driver_with_2nd_fastest_lap_time'] = d1_fastest_lap

		fl_string = f"{data['driver_with_fastest_lap']} had the fastest lap with a time of {data['driver_with_fastest_lap_time']}.\n" \
					f"This was {abs(d_fastest_time)} faster than {data['driver_with_2nd_fastest_lap']} with a time of {data['driver_with_2nd_fastest_lap_time']}\n" \
					f"(Note: these are just comparisons of these 2 drivers)"
		print(fl_string)

	@staticmethod
	def main():
		# noinspection PyTypeChecker
		api_call = Call(driver="Lewis hamilton")

		# api_call_result = api_call.drivers_for_year()
		# bs = etree.XML(api_call_result.def_return_value.content)
		# etree.indent(bs)
		# print(etree.tostring(bs, encoding='unicode'))

		api_call_result = api_call.compare_2_drivers_from_a_race(driver1='Lewis Hamilton', driver2='Max Verstappen', circut='sochi')
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
