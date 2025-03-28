import os
import requests
from typing import Tuple

APP_VERSION                   = os.getenv("APP_VERSION", "0.1-SNAPSHOT")
WEATHER_API_URL               = os.getenv("API_URL", None)
WEATHER_API_CONTENT_TYPE      = os.getenv("API_CONTENT_TYPE", "application/json")
WEATHER_API_USER_AGENT        = os.getenv("WEATHER_API_USER_AGENT", "application/json")
WEATHER_API_CONTACT_INFO      = os.getenv("WEATHER_API_CONTACT_INFO", "jorgen.finsveen@ntnu.no")
WEATHER_TEMPERATURE_THRESHOLD = int(os.getenv("WEATHER_TEMPERATURE_THRESHOLD", 0))
DISABLE_WEATHER               = bool(os.getenv('DISABLE_WEATHER', True))


def _get_weather(latitude: float, longtiude: float) -> dict:
    if WEATHER_API_URL is None:
        print("Weather error: API_URL is not set.")
        return None
    
    url = f"{WEATHER_API_URL}?lat={latitude}&lon={longtiude}"
    headers = {
        "Content-Type": WEATHER_API_CONTENT_TYPE,
        "User-Agent": f"{WEATHER_API_USER_AGENT}/{APP_VERSION} {WEATHER_API_CONTACT_INFO}"
    }

    try: 
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Weather error: {response.status_code}")
            return None
        else:
            return response.json()
    except Exception as e:
        print(f"Weather API response error: {e}")
        return None
        
            

def is_weather_ok(latitude: float, longitude: float) -> Tuple[bool, str]:
    if DISABLE_WEATHER:
        return True, "Weather check disabled"
    
    weather = _get_weather(latitude, longitude)
    
    if weather is None:
        return False, "Error fetching weather data"
    
    stats       = weather["timeseries"]["data"]["instant"]["details"]
    temperature = float(stats["air_temperature"])
    humidity    = float(stats["relative_humidity"])

    if temperature >= WEATHER_TEMPERATURE_THRESHOLD:
        return True, "Weather is good"
    else:
        return False, f"Insufficient conditions - Temperature: {temperature}, Humidity: {humidity}"
