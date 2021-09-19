import unittest
import ApiCalls

class TestMain(unittest.TestCase):

	def test_drivers_for_year(self):
		test_drivers_for_year_result = ApiCalls.Call().drivers_for_year().def_return_value
		self.assertEqual(test_drivers_for_year_result.status_code, 200)
		self.assertIsNotNone(test_drivers_for_year_result)
		self.assertTrue(len(test_drivers_for_year_result.content) > 0)

	def test_driver_information(self):
		test_driver_information_result = ApiCalls.Call(driver_id='bottas').driver_information().def_return_value
		self.assertEqual(test_driver_information_result.status_code, 200)
		self.assertIsNotNone(test_driver_information_result)
		self.assertTrue(len(test_driver_information_result.content) > 0)

	def test_constructors_for_year(self):
		test_constructors_for_year_result = ApiCalls.Call().constructors_for_year().def_return_value
		self.assertEqual(test_constructors_for_year_result.status_code, 200)
		self.assertIsNotNone(test_constructors_for_year_result)
		self.assertTrue(len(test_constructors_for_year_result.content) > 0)

	def test_circuts_for_year(self):
		test_circuts_for_year_result = ApiCalls.Call().circuts_for_year().def_return_value
		self.assertEqual(test_circuts_for_year_result.status_code, 200)
		self.assertIsNotNone(test_circuts_for_year_result)
		self.assertTrue(len(test_circuts_for_year_result.content) > 0)

	def test_results(self):
		test_results_result = ApiCalls.Call().results().def_return_value
		self.assertEqual(test_results_result.status_code, 200)
		self.assertIsNotNone(test_results_result)
		self.assertTrue(len(test_results_result.content) > 0)

	def test_schedule_for_year(self):
		test_schedule_for_year_result = ApiCalls.Call().schedule_for_year().def_return_value
		self.assertEqual(test_schedule_for_year_result.status_code, 200)
		self.assertIsNotNone(test_schedule_for_year_result)
		self.assertTrue(len(test_schedule_for_year_result.content) > 0)

	def test_season_list(self):
		test_season_list_result = ApiCalls.Call().season_list().def_return_value
		self.assertEqual(test_season_list_result.status_code, 200)
		self.assertIsNotNone(test_season_list_result)
		self.assertTrue(len(test_season_list_result.content) > 0)

	def test_qualifying_results(self):
		test_qualifying_results_result = ApiCalls.Call().qualifying_results().def_return_value
		self.assertEqual(test_qualifying_results_result.status_code, 200)
		self.assertIsNotNone(test_qualifying_results_result)
		self.assertTrue(len(test_qualifying_results_result.content) > 0)

	def test_driver_standings_after_a_race(self):
		test_driver_standings_after_a_race_result = ApiCalls.Call().driver_standings_after_a_race().def_return_value
		self.assertEqual(test_driver_standings_after_a_race_result.status_code, 200)
		self.assertIsNotNone(test_driver_standings_after_a_race_result)
		self.assertTrue(len(test_driver_standings_after_a_race_result.content) > 0)

	def test_constructor_standings_after_a_race(self):
		test_constructor_standings_after_a_race_result = ApiCalls.Call().constructor_standings_after_a_race().def_return_value
		self.assertEqual(test_constructor_standings_after_a_race_result.status_code, 200)
		self.assertIsNotNone(test_constructor_standings_after_a_race_result)
		self.assertTrue(len(test_constructor_standings_after_a_race_result.content) > 0)

	def test_current_drivers_standings(self):
		test_current_drivers_standings_result = ApiCalls.Call().current_drivers_standings().def_return_value
		self.assertEqual(test_current_drivers_standings_result.status_code, 200)
		self.assertIsNotNone(test_current_drivers_standings_result)
		self.assertTrue(len(test_current_drivers_standings_result.content) > 0)

	def test_current_constructors_standings(self):
		test_current_constructors_standings_result = ApiCalls.Call().current_constructors_standings().def_return_value
		self.assertEqual(test_current_constructors_standings_result.status_code, 200)
		self.assertIsNotNone(test_current_constructors_standings_result)
		self.assertTrue(len(test_current_constructors_standings_result.content) > 0)

	def test_all_winners_of_drivers_championships(self):
		test_all_winners_of_drivers_championships_result = ApiCalls.Call().all_winners_of_drivers_championships().def_return_value
		self.assertEqual(test_all_winners_of_drivers_championships_result.status_code, 200)
		self.assertIsNotNone(test_all_winners_of_drivers_championships_result)
		self.assertTrue(len(test_all_winners_of_drivers_championships_result.content) > 0)

	def test_all_winners_of_constructors_championships(self):
		test_all_winners_of_constructors_championships_result = ApiCalls.Call().all_winners_of_constructors_championships().def_return_value
		self.assertEqual(test_all_winners_of_constructors_championships_result.status_code, 200)
		self.assertIsNotNone(test_all_winners_of_constructors_championships_result)
		self.assertTrue(len(test_all_winners_of_constructors_championships_result.content) > 0)

	def test_driver_standings_by_specifying_the_driver(self):
		# needs driverid
		test_driver_standings_by_specifying_the_driver_result = ApiCalls.Call(driver_id='bottas').driver_standings_by_specifying_the_driver().def_return_value
		self.assertEqual(test_driver_standings_by_specifying_the_driver_result.status_code, 200)
		self.assertIsNotNone(test_driver_standings_by_specifying_the_driver_result)
		self.assertTrue(len(test_driver_standings_by_specifying_the_driver_result.content) > 0)

	def test_constructor_standings_by_specifying_the_constructor(self):
		# needs constructor_id
		test_constructor_standings_by_specifying_the_constructor_result = ApiCalls.Call(constructor_id='mclaren').constructor_standings_by_specifying_the_constructor().def_return_value
		self.assertEqual(test_constructor_standings_by_specifying_the_constructor_result.status_code, 200)
		self.assertIsNotNone(test_constructor_standings_by_specifying_the_constructor_result)
		self.assertTrue(len(test_constructor_standings_by_specifying_the_constructor_result.content) > 0)

	def test_list_of_all_finishing_status_codes(self):
		test_list_of_all_finishing_status_codes_result = ApiCalls.Call().list_of_all_finishing_status_codes().def_return_value
		self.assertEqual(test_list_of_all_finishing_status_codes_result.status_code, 200)
		self.assertIsNotNone(test_list_of_all_finishing_status_codes_result)
		self.assertTrue(len(test_list_of_all_finishing_status_codes_result.content) > 0)

	def test_list_of_finishing_status_for_a_specific_season(self):
		test_list_of_finishing_status_for_a_specific_season_result = ApiCalls.Call().list_of_finishing_status_for_a_specific_season().def_return_value
		self.assertEqual(test_list_of_finishing_status_for_a_specific_season_result.status_code, 200)
		self.assertIsNotNone(test_list_of_finishing_status_for_a_specific_season_result)
		self.assertTrue(len(test_list_of_finishing_status_for_a_specific_season_result.content) > 0)

	def test_list_of_finishing_status_for_a_specific_race_number_in_a_season(self):
		test_list_of_finishing_status_for_a_specific_race_number_in_a_season_result = ApiCalls.Call().list_of_finishing_status_for_a_specific_race_number_in_a_season().def_return_value
		self.assertEqual(test_list_of_finishing_status_for_a_specific_race_number_in_a_season_result.status_code, 200)
		self.assertIsNotNone(test_list_of_finishing_status_for_a_specific_race_number_in_a_season_result)
		self.assertTrue(len(test_list_of_finishing_status_for_a_specific_race_number_in_a_season_result.content) > 0)

	def test_lap_times(self):
		# lapnumber
		test_lap_times_result = ApiCalls.Call().lap_times().def_return_value
		self.assertEqual(test_lap_times_result.status_code, 200)
		self.assertIsNotNone(test_lap_times_result)
		self.assertTrue(len(test_lap_times_result.content) > 0)

	def test_pit_stop_data_for_a_race(self):
		test_pit_stop_data_for_a_race_result = ApiCalls.Call().pit_stop_data_for_a_race().def_return_value
		self.assertEqual(test_pit_stop_data_for_a_race_result.status_code, 200)
		self.assertIsNotNone(test_pit_stop_data_for_a_race_result)
		self.assertTrue(len(test_pit_stop_data_for_a_race_result.content) > 0)

	def test_specific_pit_stop_data_for_a_race(self):
		# pitstop_number
		test_specific_pit_stop_data_for_a_race_result = ApiCalls.Call(pitstop_number=1).specific_pit_stop_data_for_a_race().def_return_value
		self.assertEqual(test_specific_pit_stop_data_for_a_race_result.status_code, 200)
		self.assertIsNotNone(test_specific_pit_stop_data_for_a_race_result)
		self.assertTrue(len(test_specific_pit_stop_data_for_a_race_result.content) > 0)

	def test_to_string(self):
		data_to_supply = ApiCalls.Call(pitstop_number=1).specific_pit_stop_data_for_a_race()
		test_to_string_result = ApiCalls.Call().to_string(data_to_supply)
		self.assertIsNotNone(test_to_string_result)
		self.assertTrue(len(test_to_string_result) > 0)


if __name__ == "__main__":
	unittest.main()
