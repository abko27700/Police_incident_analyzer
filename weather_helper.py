import requests
from geopy.distance import geodesic
from geopy.point import Point

def get_weather_code(latitude, longitude, date):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start": date,
        "end": date,
        "hourly": "weathercode"
    }
    response = requests.get(url, params=params).json()
    # Extract the weather code from the response
    weather_code = response['hourly']['weathercode'][0]
    return weather_code