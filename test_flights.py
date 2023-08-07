
import json
import csv
import logging
import re
import pytest
from typing import List, Dict, Any

def setup_custom_logger(name, log_file, level=logging.ERROR):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_file, mode='a')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# load_json_data function 

def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    logger = setup_custom_logger('json_logger', 'app.log', level=logging.ERROR)
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data['flights']
    except FileNotFoundError as e:
        logger.error(f"File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON in file '{file_path}': {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading data: {e}")
    return []  

file_path = '/Users/sheila/Desktop/Prueba_Tecnica/data.json'
flight_records1 = load_json_data(file_path)

# Test loading JSON data function

def test_load_json_data_valid_file():
    file_path = '/Users/sheila/Desktop/Prueba_Tecnica/data.json'  
    flight_records = load_json_data(file_path)
    assert isinstance(flight_records, list)
    assert len(flight_records) > 0

def test_load_json_data_invalid_file():
    file_path = '/Users/sheila/Desktop/Prueba_Tecnica/invalid_jsonfile.json'
    flight_records = load_json_data(file_path)
    assert isinstance(flight_records, list)
    assert len(flight_records) == 0

def test_load_json_data_invalid_json():
    file_path = '/Users/sheila/Desktop/Prueba_Tecnica/invalid_jsondata.json'
    flight_records = load_json_data(file_path)
    assert isinstance(flight_records, list)
    assert len(flight_records) == 0

# load_csv_data function 

def load_csv_data(file_path: str) -> List[Dict[str, Any]]:
    logger = setup_custom_logger('csv_logger', 'app.log', level=logging.ERROR)

    flight_records2 = []
    try:
        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                flight_record = {
                    'Flight_ID': row['Flight_ID'],
                    'Passengers': int(row['Passengers']),
                    'Revenue': int(row['Revenue'])
                }
                flight_records2.append(flight_record)
        return flight_records2
    except FileNotFoundError as e:
        logger.error(f"File '{file_path}' not found.")
    except csv.Error as e:
        logger.error(f"Error reading CSV file '{file_path}': {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading data: {e}")
    return []

file_path = '/Users/sheila/Desktop/Prueba_Tecnica/data.csv'
flight_records2 = load_csv_data(file_path)

# Test loading CSV data function

def test_load_csv_data_valid_file():
    file_path = '/Users/sheila/Desktop/Prueba_Tecnica/data.csv'  
    flight_records = load_csv_data(file_path)
    assert isinstance(flight_records, list)
    assert len(flight_records) > 0

def test_load_csv_data_invalid_file():
    file_path = '/Users/sheila/Desktop/Prueba_Tecnica/invalid_csvfile.csv'
    flight_records = load_csv_data(file_path)
    assert isinstance(flight_records, list)
    assert len(flight_records) == 0

def test_load_csv_data_invalid_csv():
    file_path = '/Users/sheila/Desktop/Prueba_Tecnica/invalid_csvdata.csv'
    flight_records = load_csv_data(file_path)
    assert isinstance(flight_records, list)
    assert len(flight_records) == 0

# parse_log_data function

def parse_log_data(file_path: str) -> List[Dict[str, Any]]:
    logger = setup_custom_logger('log_parser', 'app.log', level=logging.ERROR)

    flight_records3 = []
    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                match = re.match(r'(\d{4}-\d{2}-\d{2}) (\w+) from (\w+) to (\w+) departed.', line)
                if match:
                    flight_record = {
                        'Date': match.group(1),
                        'Flight_ID': match.group(2),
                        'Departure_Airport': match.group(3),
                        'Arrival_Airport': match.group(4)
                    }
                    flight_records3.append(flight_record)
                else:
                    logger.error(f"Error parsing line: {line.strip()}")
        return flight_records3
    except FileNotFoundError as e:
        logger.error(f"File '{file_path}' not found.")
    except Exception as e:
        logger.error(f"An unexpected error occurred while parsing data: {e}")
    return []  

file_path = '/Users/sheila/Desktop/Prueba_Tecnica/data.log'
flight_records3 = parse_log_data(file_path)

# Test loading LOG data function

def test_load_log_data_valid_file():
    file_path = '/Users/sheila/Desktop/Prueba_Tecnica/data.log'  
    flight_records = parse_log_data(file_path)
    assert isinstance(flight_records, list)
    assert len(flight_records) > 0

def test_load_log_data_invalid_file():
    file_path = '/Users/sheila/Desktop/Prueba_Tecnica/invalid_logfile.log'
    flight_records = parse_log_data(file_path)
    assert isinstance(flight_records, list)
    assert len(flight_records) == 0

def test_load_csv_data_invalid_log():
    file_path = '/Users/sheila/Desktop/Prueba_Tecnica/invalid_logdata.log'
    flight_records = parse_log_data(file_path)
    assert isinstance(flight_records, list)
    assert len(flight_records) == 0

# combine_data function

def combine_data(json_data: List[Dict[str, Any]], csv_data: List[Dict[str, Any]], log_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    logger = setup_custom_logger('data_combiner', 'app.log', level=logging.ERROR)

    combined_data = []
    try:
        for json_flight in json_data:
            flight_id = json_flight['Flight_ID']
            matching_csv_flights = [flight for flight in csv_data if flight['Flight_ID'] == flight_id]
            matching_log_flights = [flight for flight in log_data if flight['Flight_ID'] == flight_id]
            if not matching_csv_flights:
                logger.error(f"CSV data not found for Flight_ID '{flight_id}'. Skipping data combination.")
                continue
            if not matching_log_flights:
                logger.error(f"Log data not found for Flight_ID '{flight_id}'. Skipping data combination.")
                continue
 
            combined_flight = {
                'Flight_ID': flight_id,
                'Date': json_flight.get('Date'),
                'Departure_Airport': json_flight.get('Departure_Airport'),
                'Arrival_Airport': json_flight.get('Arrival_Airport'),
                'Duration_Minutes': json_flight.get('Duration_Minutes'),
                'Passengers': matching_csv_flights[0].get('Passengers'),
                'Revenue': matching_csv_flights[0].get('Revenue')
            }
            combined_data.append(combined_flight)

    except Exception as e:
        logger.error(f"An unexpected error occurred while combining data: {e}")
    return combined_data

json_data = flight_records1 
csv_data = flight_records2  
log_data = flight_records3   

combined_data = combine_data(json_data, csv_data, log_data)

# Testing combine_data function 

def test_lenght_combine_data():
    combined_data = combine_data(flight_records1, flight_records2, flight_records3)
    assert len(combined_data) == len(flight_records1) == len(flight_records2) == len(flight_records3)
    
def test_keys_combine_data():
    combined_data = combine_data(flight_records1, flight_records2, flight_records3)
    expected_keys = {'Flight_ID', 'Date', 'Departure_Airport', 'Arrival_Airport', 'Duration_Minutes', 'Passengers', 'Revenue'}
    assert all(set(record.keys()) == expected_keys for record in combined_data)

def get_flight_ids(records):
    return [record['Flight_ID'] for record in records]

def test_combine_data_with_valid_data():
    combined_data = combine_data(flight_records1, flight_records2, flight_records3)

    flight_ids_1 = get_flight_ids(flight_records1)
    flight_ids_2 = get_flight_ids(flight_records2)
    flight_ids_3 = get_flight_ids(flight_records3)
    combined_flight_ids = get_flight_ids(combined_data)

    assert set(flight_ids_1) == set(flight_ids_2) == set(flight_ids_3)
    assert set(combined_flight_ids) == set(flight_ids_1)

def test_no_duplicates_in_combined_data():
    combined_data = combine_data(flight_records1, flight_records2, flight_records3)
    ids = [record['Flight_ID'] for record in combined_data]
    assert len(ids) == len(set(ids))

# calculate_revenue_per_passenger function

def calculate_revenue_per_passenger(flights_data: List[Dict[str, Any]]) -> None:
    logger = setup_custom_logger('revenue_calculator', 'app.log', level=logging.ERROR)

    try:
        for flight in flights_data:
            passengers = flight.get('Passengers')
            revenue = flight.get('Revenue')

            if passengers is not None and revenue is not None and passengers > 0:
                revenue_per_passenger = revenue / passengers
                flight['Revenue_Per_Passenger'] = revenue_per_passenger
            else:
                logger.error(f"Invalid data for Flight_ID '{flight.get('Flight_ID')}'. Unable to calculate 'Revenue_Per_Passenger'.")

    except Exception as e:
        logger.error(f"An unexpected error occurred while calculating 'Revenue_Per_Passenger': {e}")

flights_data = combined_data

calculate_revenue_per_passenger(flights_data)

# Testing revenue_per_passenger

def test_calculate_revenue_per_passenger_empty_data():
    flights_data = []
    calculate_revenue_per_passenger(flights_data)
    assert len(flights_data) == 0 

def test_calculate_revenue_per_passenger_valid_data():
    flights_data = [
        {'Flight_ID': 1, 'Passengers': 100, 'Revenue': 2000},
        {'Flight_ID': 2, 'Passengers': 50, 'Revenue': 1000},
    ]
    calculate_revenue_per_passenger(flights_data)
    assert 'Revenue_Per_Passenger' in flights_data[0]
    assert 'Revenue_Per_Passenger' in flights_data[1]
    assert flights_data[0]['Revenue_Per_Passenger'] == 20.0
    assert flights_data[1]['Revenue_Per_Passenger'] == 20.0

def test_calculate_revenue_per_passenger_missing_data():
    flights_data = [
        {'Flight_ID': 1, 'Revenue': 2000},
        {'Flight_ID': 2, 'Passengers': 100, 'Revenue': None},
    ]
    calculate_revenue_per_passenger(flights_data)
    assert 'Revenue_Per_Passenger' not in flights_data[0]
    assert 'Revenue_Per_Passenger' not in flights_data[1]
