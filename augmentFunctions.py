import csv
from datetime import datetime
import requests
from geopy.geocoders import Nominatim
from dateutil import parser
from geopy.distance import geodesic
import dbOperations
from dbOperations import get_nature_rankings,get_location_rankings,check_coordinates_in_db,insert_coordinates_to_db
import math
import time
import googlemaps
import logger

google_api_key="AIzaSyAgcKWzmmxgDRVuH_IDrCNPRkdXtLOF9pg"
#this should be done by whoever is calling this file, dont invoke nominatim multiple times. the coordinates are prepassed.
def get_location(location_str):
    logger.log_message("Trying to get location "+location_str)
    #Process the string. Empty  or coodinates or / in between.
    if not location_str.strip():
        # logger.log_message("Empty location string provided; defaulting to Norman.")
        return get_location("Norman")

    if ';' in location_str:
        # Split the coordinates into latitude and longitude
        latitude, longitude = location_str.split(';')
        return float(latitude), float(longitude)

    if '/' in location_str:
        # Take only the part before the '/'
        location_str = location_str.split('/')[0]
        logger.log_message("Modified location string to use: " + location_str)
    
    latitude, longitude, status = check_coordinates_in_db(location_str)
    if status == 0:
        return latitude, longitude
    else:
        try:
            logger.log_message("Sleeping for 1 second")  
            time.sleep(1.1)
            geolocator = Nominatim(user_agent="augmentor_1")
            location = geolocator.geocode(location_str)
            logger.log_message("GEOCODER: fetched new coordinates for " + location_str)
            if location:
                insert_coordinates_to_db(location_str, location.latitude, location.longitude)
                return location.latitude, location.longitude
            else:
                logger.log_message("Error in fetching coordinates for location "+ location_str)
                #try fetching coordinates using google location service. 
                return get_location_using_google_maps(location_str, google_api_key)
                # return get_location("Norman")
        except Exception as e:
            logger.log_message(f"GEOCODER: service Error: {e}")
            logger.log_message("Error in fetching coordinates for location "+ location_str)
            #try fetching coordinates using google location service. 
            return get_location_using_google_maps(location_str, google_api_key)

def get_location_using_google_maps(location_str, api_key):
    gmaps = googlemaps.Client(key=api_key)
    try:
        result = gmaps.geocode(location_str)
        if result:
            latitude = result[0]['geometry']['location']['lat']
            longitude = result[0]['geometry']['location']['lng']
            logger.log_message("Fetched coordinates from Google Maps for " + location_str)
            insert_coordinates_to_db(location_str, latitude, longitude)
            return latitude, longitude
        else:
            logger.log_message("Google Maps could not find location: "+ location_str)
            return get_location("Norman")
    except Exception as e:
        logger.log_message(f"Error with Google Maps API: {e}")
        return get_location("Norman")
    
# Dummy function placeholders for unimplemented logic
def get_weather_code(latitude, longitude, date, hour):
    url = "https://archive-api.open-meteo.com/v1/archive"
    # Construct the URL with parameters appended
    url += f"?latitude={latitude}&longitude={longitude}&start_date={date}&end_date={date}&hourly=weather_code"
    # logger.log_message(url)
    # logger.log_message("https://archive-api.open-meteo.com/v1/archive?latitude=40.741059199999995&longitude=-73.98964162240998&start_date=2024-03-03&end_date=2024-03-03&hourly=weather_code")
    # logger.log_message("https://archive-api.open-meteo.com/v1/archive?latitude=40.741059199999995&longitude=-73.98964162240998&start_date=2024-03-03&end_date=2024-03-03&hourly=weather_code")
    try:
        response = requests.get(url).json()
        # logger.log_message(response)
        # Extract weather codes from the response
        hourly_data = response.get('hourly', {})
        time_list = hourly_data.get('time', [])
        weather_code_list = hourly_data.get('weather_code', [])
        
        # Convert the specified date and hour into a datetime object
        target_datetime = parser.parse(f"{date}T{hour:02d}:00")
        
        # Iterate through the times to find the index for the specified hour
        for i, time_str in enumerate(time_list):
            time_datetime = parser.parse(time_str)
            if time_datetime == target_datetime:
                weather_code = weather_code_list[i]
                return weather_code
        
        logger.log_message("Weather code for the specified time not found.")
        logger.log_message(url)
        logger.log_message(response)
        return None
    except requests.RequestException as e:
        logger.log_message(f"Request failed: {e}")
        return None

def get_location_rank(location_rankings, incident_location_address):
    """
    Returns the rank of the incident location based on its address.
    
    Parameters:
    - location_rankings: A dictionary where keys are addresses of incident locations and values are their ranks.
    - incident_location_address: The address of the incident location to get the rank for.
    
    Returns:
    - The rank of the location if found in the location_rankings, or 0 if not found.
    """
    # Check if the incident location address exists in the rankings and return its rank
    return location_rankings.get(incident_location_address, 0)


def get_side_of_town(location_latitude,location_longitude):
    center_address="Norman"
    center_latitude,center_longitude=get_location(center_address)


    # Calculate the bearing from the center to the given location
    center_point = (center_latitude, center_longitude)
    location_point = (location_latitude, location_longitude)
    bearing = calculate_bearing(center_point, location_point)

    # Determine the side of town based on the bearing
    if 22.5 <= bearing < 67.5:
        return "NE"
    elif 67.5 <= bearing < 112.5:
        return "E"
    elif 112.5 <= bearing < 157.5:
        return "SE"
    elif 157.5 <= bearing < 202.5:
        return "S"
    elif 202.5 <= bearing < 247.5:
        return "SW"
    elif 247.5 <= bearing < 292.5:
        return "W"
    elif 292.5 <= bearing < 337.5:
        return "NW"
    else:
        return "N"

def calculate_bearing(point1, point2):
    """
    Calculate the bearing between two geographical points.
    """
    lat1, lon1 = point1
    lat2, lon2 = point2

    delta_lon = lon2 - lon1

    x = (math.cos(math.radians(lat2)) * math.sin(math.radians(delta_lon)))
    y = (math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) -
         math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(delta_lon)))

    bearing = math.atan2(x, y)

    # Convert radians to degrees
    bearing = math.degrees(bearing)

    # Normalize bearing to range [0, 360)
    bearing = (bearing + 360) % 360

    return bearing


def get_incident_rank(nature_rankings,nature):
    # Placeholder for ranking the incident
    # Implementation would be based on predefined rules or categories
    return nature_rankings.get(nature, 0)

def check_ems_stat(current_incident_id, incident_location):
    """
    Check if the EMSSTAT condition is met for an incident based on its location and surrounding incidents.
    
    Parameters:
    - current_incident_id: The database ID of the current incident.
    - incident_location: The location of the current incident.
    
    Returns:
    - True if EMSSTAT conditions are met, False otherwise.
    """
    # Fetch a window of incidents around the current one, ordered by time.
    incidents = dbOperations.fetch_incident_window(current_incident_id, window_size=3)

    # Filter incidents by location
    location_matches = [incident for incident in incidents if incident[3] == incident_location]

    # Check the ORI for the current and surrounding incidents at the same location
    for incident in location_matches:
        if incident[5] == "EMSSTAT":  # Assuming [5] is the index for incident_ori
            return True

    return False


def get_day_of_week(date_str):
      # Ensure date is in "yyyy-mm-dd" format
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # Adjusting the calculation to fit your specified logic
    return (date_obj.weekday() + 1) % 7 + 1

def get_time_of_day(time_str):
    hour = int(time_str.split(':')[0])
    return hour

def augment_data():
    nature_rankings=get_nature_rankings()
    location_rankings=get_location_rankings()
    incidents=dbOperations.get_incidents_from_database()
    with open('augmented_incidents.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        logger.log_message(("Day\tTime\tWeather\tLocationRank\tSide of Town\tIncident Rank\tNature\tEMSSTAT"))
        print(("Day\tTime\tWeather\tLocationRank\tSide of Town\tIncident Rank\tNature\tEMSSTAT"))
        writer.writerow(["Day", "Time", "Weather", "LocationRank", "Side of Town", "Incident Rank", "Nature", "EMSSTAT"])
        for row in incidents:
            incident_id=row[0]
            incident_time = row[1]  
            incident_number = row[2]  
            incident_location_address = row[3]  
            incident_nature = row[4]  
            incident_ori = row[5] 
            incident_datetime = datetime.strptime(incident_time, "%m/%d/%Y %H:%M")
            # Extract date in yyyy-mm-dd format
            incident_date_formatted = incident_datetime.strftime("%Y-%m-%d")
            # Extract time
            incident_time_formatted = incident_datetime.strftime("%H:%M")
            location_latitude,location_longitude = get_location(incident_location_address)

            day_of_week = get_day_of_week(incident_date_formatted)
            time_of_day = get_time_of_day(incident_time_formatted)
            weather = get_weather_code(location_latitude, location_longitude, incident_date_formatted, time_of_day)
            location_rank=get_location_rank(location_rankings,incident_location_address)
            side_of_town=get_side_of_town(location_latitude,location_longitude)
            nature=incident_nature
            incident_rank=get_incident_rank(nature_rankings,nature)

            emsstat= check_ems_stat(incident_id,incident_location_address)
            logger.log_message(f"{incident_number}\t{day_of_week}\t{time_of_day}\t{weather}\t{location_rank}\t{side_of_town}\t{incident_rank}\t{nature}\t{int(emsstat)}")
            print(f"{incident_number}\t{day_of_week}\t{time_of_day}\t{weather}\t{location_rank}\t{side_of_town}\t{incident_rank}\t{nature}\t{int(emsstat)}")
            writer.writerow([incident_number,day_of_week, time_of_day, weather, location_rank, side_of_town, incident_rank, incident_nature, int(emsstat)])