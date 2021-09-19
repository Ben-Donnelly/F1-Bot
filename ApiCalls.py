from requests import get
from lxml import etree
from datetime import datetime


class Call:
	current_year = datetime.today().year

	def __init__(self, year=current_year, race_number=None, driver=None):
		self.year = year
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

		api_call_result = api_call.compare_2_drivers_from_a_race(driver1='Lewis Hamilton', driver2='Max Verstappen', circuit='sochi')
		# print(api_call_result)

		# print(api_call_result.def_return_value.content)
		# root = ET.fromstring(api_call_result.def_return_value.text)
		# print(root.findall("[tag='Driver']"))

		api_call_result = api_call.driver_standings_by_specifying_the_driver()

		print(api_call.to_string(api_call_result))


if __name__ == "__main__":
	call = Call()
	call.main()
