from requests import get
from bs4 import BeautifulSoup
from lxml import etree

def driversForYear(year):
	drivers_root_get = get(f"http://ergast.com/api/f1/{year}/drivers")
	return etree.fromstring(drivers_root_get.content)


def constructorsForYear(year, round=None):

	# There isn't much point in this? No team has ever pulled out halfway through a season?
	if round:
		constructors_root = get(f"http://ergast.com/api/f1/{year}/{round}/constructors")
	else:
		constructors_root = get(f"http://ergast.com/api/f1/{year}/constructors")
	return etree.fromstring(constructors_root.content)


def circutsForYear(year, round=None):
	# This is a bit more useful as it dosent seem that the circuts are in race order, but alphabetical
	if round:
		circuts_root = get(f"http://ergast.com/api/f1/{year}/{round}/circuits")
	else:
		circuts_root = get(f"http://ergast.com/api/f1/{year}/circuits")
	# TODO: Special characters (e.g. ü) print in unicode, fix
	return etree.fromstring(circuts_root.content)


def results(year, round):
	# This is cool
	results_root = get(f"http://ergast.com/api/f1/{year}/{round}/results")
	return etree.fromstring(results_root.content)

# Ignore the type hint here
def scheduleForYear(year="current"):
	# This has date and time
	schedule_root = get(f"http://ergast.com/api/f1/{year}")
	return etree.fromstring(schedule_root.content)

def main():
	# Next: Driver standings after a race
	print(etree.tostring(scheduleForYear(2019), pretty_print=True).decode())

if __name__ == "__main__":
	main()