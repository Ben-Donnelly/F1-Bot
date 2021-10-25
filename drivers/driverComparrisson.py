from datetime import datetime
from results import results
from drivers import F1drivers


class DriverCompare:
	current_year = datetime.today().year

	def __init__(self, driver1, driver2, circuit=None):
		self.results_call = results.Results()
		self.kph_to_mph = 1.609344
		self.driver1 = driver1
		self.driver2 = driver2
		self.circuit = circuit


	def compare_2_drivers_from_a_race(self):
		if not self.driver1 or not self.driver2 or not self.circuit:
			raise Exception('You need to specify 2 drivers to compare and a a circuit')

		data = self.results_call.results(compare_driver1=self.driver1, compare_driver2=self.driver2, circuit=self.circuit, compare_flag=True)
		d1, d2 = data.keys()

		d1_fastest_lap = data[d1]['FastestLap']['Time']['time']
		d1_fastest_lap_rank = data[d1]['FastestLap']['rank']
		d1_fastest_lap_lap_number = data[d1]['FastestLap']['lap']
		d1_fastest_lap_avg_speed_kph = float(data[d1]['FastestLap']['AverageSpeed']['speed'])


		d2_fastest_lap = data[d2]['FastestLap']['Time']['time']
		d2_fastest_lap_rank = data[d2]['FastestLap']['rank']
		d2_fastest_lap_lap_number = data[d2]['FastestLap']['lap']
		d2_fastest_lap_avg_speed_kph = float(data[d2]['FastestLap']['AverageSpeed']['speed'])

		format = '%M:%S.%f'
		d_fastest_time = (datetime.strptime(d1_fastest_lap, format) - datetime.strptime(d2_fastest_lap, format)).total_seconds()
		driver_comparison_dict = {}
		if d_fastest_time < 0:
			driver_comparison_dict['driver_with_fastest_lap'] = d1
			driver_comparison_dict['driver_with_fastest_lap_time'] = d1_fastest_lap
			driver_comparison_dict['driver_with_fastest_lap_rank'] = d1_fastest_lap_rank
			driver_comparison_dict['driver_with_fastest_lap_lap_number'] = d1_fastest_lap_lap_number
			driver_comparison_dict['driver_with_fastest_lap_avg_kph'] = d1_fastest_lap_avg_speed_kph
			driver_comparison_dict['driver_with_2nd_fastest_lap'] = d2
			driver_comparison_dict['driver_with_2nd_fastest_lap_time'] = d2_fastest_lap
			driver_comparison_dict['driver_with_2nd_fastest_lap_rank'] = d2_fastest_lap_rank
			driver_comparison_dict['driver_with_2nd_fastest_lap_lap_number'] = d2_fastest_lap_lap_number
			driver_comparison_dict['driver_with_2nd_fastest_lap_avg_kph'] = d2_fastest_lap_avg_speed_kph
		else:
			driver_comparison_dict['driver_with_fastest_lap'] = d2
			driver_comparison_dict['driver_with_fastest_lap_time'] = d2_fastest_lap
			driver_comparison_dict['driver_with_fastest_lap_rank'] = d2_fastest_lap_rank
			driver_comparison_dict['driver_with_fastest_lap_lap_number'] = d2_fastest_lap_lap_number
			driver_comparison_dict['driver_with_fastest_lap_avg_kph'] = d2_fastest_lap_avg_speed_kph
			driver_comparison_dict['driver_with_2nd_fastest_lap'] = d1
			driver_comparison_dict['driver_with_2nd_fastest_lap_time'] = d1_fastest_lap
			driver_comparison_dict['driver_with_2nd_fastest_lap_rank'] = d1_fastest_lap_rank
			driver_comparison_dict['driver_with_2nd_fastest_lap_lap_number'] = d1_fastest_lap_lap_number
			driver_comparison_dict['driver_with_2nd_fastest_lap_avg_kph'] = d1_fastest_lap_avg_speed_kph


		fl_string = f"{driver_comparison_dict['driver_with_fastest_lap']} had the fastest lap with a time of {driver_comparison_dict['driver_with_fastest_lap_time']}.\n" \
					f"This was {abs(d_fastest_time)} faster than {driver_comparison_dict['driver_with_2nd_fastest_lap']} with a time of {driver_comparison_dict['driver_with_2nd_fastest_lap_time']}\n" \
					f"{driver_comparison_dict['driver_with_fastest_lap']} fastest lap rank: {driver_comparison_dict['driver_with_fastest_lap_rank']} " \
					f"{driver_comparison_dict['driver_with_2nd_fastest_lap']} fastest lap rank: {driver_comparison_dict['driver_with_2nd_fastest_lap_rank']}\n"\
					f"{driver_comparison_dict['driver_with_fastest_lap']} fastest lap avg speed: {driver_comparison_dict['driver_with_fastest_lap_avg_kph']}kph ({(driver_comparison_dict['driver_with_fastest_lap_avg_kph']/self.kph_to_mph):.2f}mph) " \
					f"{driver_comparison_dict['driver_with_2nd_fastest_lap']} fastest lap avg speed: {driver_comparison_dict['driver_with_2nd_fastest_lap_avg_kph']}kph ({(driver_comparison_dict['driver_with_2nd_fastest_lap_avg_kph']/self.kph_to_mph):.2f}mph) "
		print(fl_string)

	def compare_2_drivers(self):
		f1_driver_call = F1drivers.Drivers(self.driver1)
		f1_driver_call.driver_information()



