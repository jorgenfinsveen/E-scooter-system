import logging
from api.mqtt import MQTTClient
from controller.MainController import MainController

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
    return [t0, t1, t2, t3]

class WeatherLock:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.stm = None
        self.mqtt_client = MQTTClient()
        self.controller = MainController()

    def request_temperature(self):
        self.controller.request_temperature()
    
    def lock_scooter(self):
        self._logger.warning("Locking the scooter due to weather conditions")
        self.mqtt_client.abort_session(cause="weather")
        self.controller.lock()
