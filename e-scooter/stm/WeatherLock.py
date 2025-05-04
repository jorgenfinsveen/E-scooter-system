import logging

from api.mqtt import MQTTClient
from tools.observer import State

# States
t0 = {
    'source': 'initial',
    'target': 'idle',
    'effect': 'start_timer("t", 3_000)'
}

t1 = {
    'source':  'idle',
    'target':  'awaiting-weather-report',
    'effect':  'request_temperature()',
    'trigger': 't'
}

t2 = {
    'source':  'awaiting-weather-report',
    'target':  'idle',
    'effect':  'start_timer("t", 3_000)',
    'trigger': 'temperature_valid'
}

t3 = {
    'source':  'awaiting-weather-report',
    'target':  'locked',
    'effect':  'lock_scooter()',
    'trigger': 'temperature_invalid'
}


def getWeatherTransitions():
    """
    Returns the state machine transitions for the weather lock.
    """
    return [t0, t1, t2, t3]

class WeatherLock:
    """
    The WeatherLock class manages the state machine for weather conditions.
    It locks the scooter if the temperature is below a certain threshold.
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.stm = None
        self._mqtt_client = MQTTClient()
        self._state = State()

    def request_temperature(self):
        """
        Request a temperature analysis from the main-controller.
        """
        self._state.set("awaiting-weather-report")
    
    def lock_scooter(self):
        """
        Lock the scooter and abort the session.
        """
        self._logger.warning("Locking the scooter due to weather conditions")
        self._mqtt_client.abort_session(cause="weather")
        self._state.set("locked")
