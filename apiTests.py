import unittest
import ApiCalls

class TestMain(unittest.TestCase):

	def test_drivers_for_year(self):
		test_drivers_for_year_result = ApiCalls.Calls().drivers_for_year().def_return_value
		self.assertEquals(test_drivers_for_year_result.status_code, 200)
		self.assertIsNotNone(test_drivers_for_year_result)
		self.assertTrue(len(test_drivers_for_year_result.content) > 0)


	def test_driver_information(self):
		test_driver_information_result = ApiCalls.Calls().driver_information('gasly').def_return_value
		self.assertEquals(test_driver_information_result.status_code, 200)
		self.assertIsNotNone(test_driver_information_result)
		self.assertTrue(len(test_driver_information_result.content) > 0)

	def test_constructors_for_year(self):
		pass

	def test_circuts_for_year(self):
		pass

	def test_results(self):
		pass

	def test_schedule_for_year(self):
		pass

	def test_season_list(self):
		pass

	def test_qualifying_results(self):
		pass

	def test_driver_standings_after_a_race(self):
		pass

	def test_constructor_standings_after_a_race(self):
		pass

	def test_current_drivers_standings(self):
		pass

	def test_current_constructors_standings(self):
		pass

	def test_all_winners_of_drivers_championships(self):
		pass

	def test_all_winners_of_constructors_championships(self):
		pass

	def test_driver_standings_by_specifying_the_driver(self):
		# needs driverid
		pass

	def test_constructor_standings_by_specifying_the_constructor(self):
		# needs constructor_id
		pass

	def test_list_of_all_finishing_status_codes(self):
		pass

	def test_list_of_finishing_status_for_a_specific_season(self):
		pass

	def test_list_of_finishing_status_for_a_specific_race_number_in_a_season(self):
		pass

	def test_lap_times(self):
		# lapnumber
		pass

	def test_pit_stop_data_for_a_race(self):
		pass

	def test_specific_pit_stop_data_for_a_race(self):
		# pitstop_number
		pass

	def test_to_string(data):
		pass

if __name__ == "__main__":
	unittest.main()