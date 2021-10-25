from datetime import datetime
from circuits import circuits
from drivers import driverComparrisson, F1drivers
from results import results

class Call:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None):

		self.year = year
		self.race_number = race_number
		self.base_url = "http://ergast.com/api/f1"
		self.extra_information = ""
		self.return_values = {}

	def validate_parameters(self):
		if self.race_number == 'last':
			self.extra_information = f"You did not specify a race number, so I got the information for the last race\n"
	@staticmethod
	def error_message(message):
		print(message)
		exit()

	def drivers_call(self):
		driverCall = circuits.Circuits()
		driverCall.circuits_for_year()

	@staticmethod
	def main():
		# noinspection PyTypeChecker
		# api_call = driverComparrisson
		api_call = F1drivers

		# api_call_result = api_call.drivers_for_year()
		# bs = etree.XML(api_call_result.def_return_value.content)
		# etree.indent(bs)
		# print(etree.tostring(bs, encoding='unicode'))
		api_call.Drivers('Max Verstappen').driver_information()

		# api_call_result = api_call.compare_2_drivers_from_a_race(driver1='Lewis Hamilton', driver2='Max Verstappen', circuit='sochi')
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
