# run_tests.py

import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# test_assignment2.py

import augmentor
import dbOperations
import augmentFunctions
def test_read_csv():
    expected_urls = [
        "https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-01_daily_incident_summary.pdf",
        "https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-02_daily_incident_summary.pdf",
        "https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-03_daily_incident_summary.pdf"
       ]
    assert augmentor.read_csv('testCsv.csv') == expected_urls

def test_get_day_of_week():
    assert augmentFunctions.get_day_of_week('2024-02-01')==5

def test_get_time_of_day():
    assert augmentFunctions.get_time_of_day('23:45')==23

def test_get_location():
    assert augmentFunctions.get_location('Norman')==(35.2225717, -97.4394816)

def test_get_weather_code():
    assert augmentFunctions.get_weather_code(35.2225717, -97.4394816, '2024-02-01', 2)==1

def test_get_side_of_town():
    assert augmentFunctions.get_side_of_town(35.2225717, -97.4394816)=='N'


def main():
    test_read_csv()
    test_get_day_of_week()
    test_get_time_of_day()
    test_get_location()
    test_get_weather_code()
    test_get_side_of_town()


if __name__ == "__main__":
   main()
