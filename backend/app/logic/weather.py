import os
import logging
import requests

APP_VERSION                   = os.getenv("APP_VERSION", "0.1-SNAPSHOT")
WEATHER_API_URL               = os.getenv("WEATHER_API_URL", None)
WEATHER_API_CONTENT_TYPE      = os.getenv("WEATHER_API_CONTENT_TYPE", "application/json")
WEATHER_API_USER_AGENT        = os.getenv("WEATHER_API_USER_AGENT", "application/json")
WEATHER_API_CONTACT_INFO      = os.getenv("WEATHER_API_CONTACT_INFO", "jorgen.finsveen@ntnu.no")
WEATHER_TEMPERATURE_THRESHOLD = int(os.getenv("WEATHER_TEMPERATURE_THRESHOLD", 0))
DISABLE_WEATHER = os.getenv("DISABLE_WEATHER", "False").lower() == "true"

logger = logging.getLogger(__name__)



def _get_weather(latitude: float, longtiude: float) -> dict:
    """
    Internal function fecthing weather data from the specified weather forecast API.
    The API URL is set in the environment variable WEATHER_API_URL.
    API used for this project is the MET API from Norway. Using other APIs may require
    different parameters and headers and result in different JSON format.

    See:
        * <a href="https://api.met.no/weatherapi/documentation">api.met.no</a>
    Args:
        latitude (float): Latitude of the location.
        longtiude (float): Longitude of the location.
    Returns:
        dict: Weather data in JSON format.
    """
    if WEATHER_API_URL is None:
        logger.error("API_URL is not set.")
        return None
    
    url = f"{WEATHER_API_URL}?lat={latitude}&lon={longtiude}"
    headers = {
        "Content-Type": WEATHER_API_CONTENT_TYPE,
        "User-Agent": f"{WEATHER_API_USER_AGENT}/{APP_VERSION} {WEATHER_API_CONTACT_INFO}"
    }

    try: 
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(f"Invalid response code: {response.status_code}")
            return None
        else:
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return None
        
            

def is_weather_ok(latitude: float, longtitude: float) -> tuple[bool, str, str]:
    """
    Check if the weather conditions are acceptable for scooter usage.
    Wether conditions are considered acceptable if the temperature is above the
    threshold set in the environment variable WEATHER_TEMPERATURE_THRESHOLD.
    The temperature is fetched from the MET API.
    Args:
        latitude (float): Latitude of the location.
        longtitude (float): Longtitude of the location.
    Returns:
        Tuple: 
         * [0]: _bool_. True if the weather conditions are acceptable, False otherwise.
         * [1]: _str_. A message indicating the result of the weather check.
        
        __Example__
    ```python
        is_weather_ok(63.41947, 10.40174) ->
        (True, "Acceptable conditions - Temperature: 15.0, Humidity: 50.0")
    ```
    """
    if DISABLE_WEATHER:
        return True, "weather check disabled", ""
    
    weather = _get_weather(latitude, longtitude)

    if weather is None:
        return False, "error fetching weather data", "bad-weather"

    stats       = weather["properties"]["timeseries"][0]["data"]["instant"]["details"]
    temperature = float(stats["air_temperature"])
    humidity    = float(stats["relative_humidity"])

    if temperature >= WEATHER_TEMPERATURE_THRESHOLD:
        return True, f"acceptable conditions <br/> temperature: {temperature} <br/> humidity: {humidity}", ""
    else:
        return False, f"insufficient conditions <br/> Temperature: {temperature} <br/> humidity: {humidity}", "bad-weather"
