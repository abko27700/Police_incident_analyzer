# README

## NAME: Abhishek Kothari
## UFID: 35641285


## Assignment Description:
In this assignment, we will perform a subsequent task for the data pipeline. Using the submission from assignment 0 we will take records from several instances of pdf files and augment the data. We will also create a Datasheet for the dataset you creating. 

## How to install
On an ubuntu server: 
'sudo apt install zlib1g zlib1g-dev libssl-dev libbz2-dev libsqlite3-dev libncurses5-dev libssl-dev liblzma-dev libffi-dev libreadline-dev'
curl https://pyenv.run | bash
pyenv install 3.11
pyenv global 3.11
pipenv install pypdf 
pipenv install --dev pytest
pipenv install requests pysqlite3 pypdf geopy googlemaps

## How to run
pipenv run python assignment2.py --urls files.csv

https://github.com/bkothariufl/cis6930sp24-assignment2/assets/151199302/33b7660e-dac0-40d9-8166-1c5fdefdcea7

## assginment2.py Function Descriptions

### `read_csv(file_path: str) -> List[str]`
Reads a CSV file containing PDF URLs and returns a list of URLs.

### `extract_date_from_url(url: str) -> str`
Extracts the date from the provided URL. If the date is not found or not in the format of yyyy-mm-dd, it retrieves the name of the file.

### `download_pdf(url: str, dest_path: str) -> str`
Downloads a PDF file from the specified URL, saves it to the destination folder, and returns the path to the downloaded file. If an error occurs during the download, it prints an error message.

### `parse_pdf(file_path: str) -> List[Tuple[str, str, str, str, str]]`
Parses the content of a PDF file specified by the file path and returns a list of tuples containing incident data such as incident time, incident number, incident location, nature, and incident origin.

### `processPdfs(file_path: str)`
Processes the PDFs listed in the CSV file. It downloads each PDF, parses its content, inserts the parsed data into a SQLite database, augments the data, and then deletes the temporary files.

### `clear_log_file(log_file_path: str)`
Clears the content of the log file.

### `main()`
The main function that handles command-line arguments and initiates the PDF processing workflow.

## dbOperations.py Function Descriptions

### `destroy_db()`
Destroys the SQLite database file 'resources/normanpd.db' if it exists.

### `createDb()`
Creates a SQLite database file 'resources/normanpd.db' and an 'incidents' table within it if they do not exist already. The table includes columns for incident details such as incident time, incident number, incident location, nature, and incident origin.

### `insertIntoDb(parsed_data: List[Tuple[str, str, str, str, str]])`
Inserts the parsed incident data into the SQLite database. Expects a list of tuples representing incident details.

### `generate_report() -> str`
Generates a report based on the data in the 'incidents' table. The report includes the count of incidents grouped by nature and is ordered by ID in ascending order.

### `get_nature_frequencies() -> List[Tuple[str, int]]`
Retrieves the frequencies of different incident natures from the database and returns a list of tuples containing each nature and its corresponding frequency, sorted by frequency in descending order.

### `assign_nature_rankings(sorted_natures: List[Tuple[str, int]]) -> Dict[str, int]`
Assigns rankings to incident natures based on their frequencies. Expects a sorted list of tuples containing incident natures and their frequencies, and returns a dictionary mapping each nature to its ranking.

### `get_location_frequencies() -> List[Tuple[str, int]]`
Retrieves the frequencies of different incident locations from the database and returns a list of tuples containing each location and its corresponding frequency, sorted by frequency in descending order.

### `assign_location_rankings(sorted_locations: List[Tuple[str, int]]) -> Dict[str, int]`
Assigns rankings to incident locations based on their frequencies. Expects a sorted list of tuples containing incident locations and their frequencies, and returns a dictionary mapping each location to its ranking.

### `get_nature_rankings() -> Dict[str, int]`
Retrieves the rankings of incident natures and returns a dictionary mapping each nature to its ranking.

### `get_location_rankings() -> Dict[str, int]`
Retrieves the rankings of incident locations and returns a dictionary mapping each location to its ranking.

### `get_incidents_from_database() -> List[Tuple]`
Retrieves all incidents from the database and returns them as a list of tuples.

### `create_coordinates_db()`
Creates a SQLite database file 'resources/coordinates.db' and a 'coordinates' table within it if they do not exist already. The table includes columns for location name, latitude, and longitude.

### `check_coordinates_in_db(location_str: str) -> Tuple[Optional[float], Optional[float], int]`
Checks if the coordinates for a given location name exist in the database. Returns the latitude and longitude if found, along with a status code indicating the result.

### `insert_coordinates_to_db(name: str, latitude: float, longitude: float)`
Inserts the coordinates of a location into the 'coordinates' table of the SQLite database. Expects the location name, latitude, and longitude as arguments.

### `fetch_incident_window(current_incident_id: int, window_size: int = 3) -> List[Tuple]`
Fetches a window of incidents centered around the specified incident ID from the database. Returns the incidents within the specified window size as a list of tuples.

## augmentFunctions.py Function Descriptions

### `get_location(location_str: str) -> Tuple[Optional[float], Optional[float]]`
Attempts to retrieve the latitude and longitude coordinates for a given location string. If the coordinates are found in the catched database, they are returned. Otherwise, the geocoding service (Nominatim) is used to fetch the coordinates. If the geocoding service fails, Google Maps is used as a fallback. Returns a tuple of latitude and longitude.

### `get_location_using_google_maps(location_str: str, api_key: str) -> Tuple[Optional[float], Optional[float]]`
Uses the Google Maps API to fetch the latitude and longitude coordinates for a given location string. Returns a tuple of latitude and longitude.

### `get_weather_code(latitude: float, longitude: float, date: str, hour: int) -> Optional[int]`
Fetches the weather code for a specific location, date, and hour using the Open Meteo Archive API. Returns the weather code if successful, otherwise returns None.

### `get_location_rank(location_rankings: Dict[str, int], incident_location_address: str) -> int`
Retrieves the rank of the incident location address from the provided location rankings dictionary. Returns the location rank.

### `get_side_of_town(location_latitude: float, location_longitude: float) -> str`
Determines the side of town (directional label) based on the latitude and longitude of a location relative to Norman, Oklahoma. Returns a string representing the side of town.

### `calculate_bearing(point1: Tuple[float, float], point2: Tuple[float, float]) -> float`
Calculates the bearing (direction) between two geographical points. Returns the bearing in degrees.

### `get_incident_rank(nature_rankings: Dict[str, int], nature: str) -> int`
Retrieves the rank of the incident nature from the provided nature rankings dictionary. Returns the incident rank.

### `check_ems_stat(current_incident_id: int, incident_location: str) -> bool`
Checks if an EMSSTAT incident occurred at the same location within a window of incidents centered around the current one. Returns True if an EMSSTAT incident is found, otherwise returns False.

### `get_day_of_week(date_str: str) -> int`
Converts a date string in "yyyy-mm-dd" format to the day of the week (1-7, where Monday is 1). Returns the day of the week.

### `get_time_of_day(time_str: str) -> int`
Extracts the hour from a time string in "HH:MM" format. Returns the hour.

### `augment_data()`
Augments incident data by fetching additional information such as day of the week, time of day, weather, location rank, side of town, incident rank, and EMSSTAT status. Writes the augmented data to a CSV file named 'augmented_incidents.csv' and also prints it to the console..



## Bugs and Assumptions:
Default Location Assumption: The code defaults to Norman, Oklahoma, when it encounters an empty location string or fails to retrieve coordinates for a given location. This assumes that incidents without specified locations or with invalid locations should be attributed to Norman, which may not always be accurate.

Geocoding Service Reliability: The code relies on external geocoding services (Nominatim and Google Maps) to fetch coordinates for location strings. It assumes that these services are always available and accurate. However, there may be cases where the services are temporarily unavailable or return incorrect results, leading to inaccurate coordinates.

Weather Data Availability: The code fetches weather codes for specific locations, dates, and hours using an external API (Open Meteo Archive). It assumes that weather data for the specified parameters is always available and accurate. However, if the API fails to provide weather data or returns incorrect information, it may affect the accuracy of the augmented incident data. 