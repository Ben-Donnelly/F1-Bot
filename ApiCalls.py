from requests import get
from lxml import etree
from datetime import datetime

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
		api_call = Call(race_number=4)

		api_call_result = api_call.driver_standings_by_specifying_the_driver()

		print(api_call.to_string(api_call_result))


if __name__ == "__main__":
	call = Call()
	call.main()
