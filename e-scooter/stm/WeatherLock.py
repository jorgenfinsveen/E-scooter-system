import logging
from api.mqtt import MQTTClient
from controller.MainController import MainController


t0 = {
    'source': 'initial',
    'target': 'locked',
}

t1 = {
    'trigger': 'unlock',
    'source': 'locked',
    'target': 'unlocked',
    'effect': 'unlock()'
}

t2 = {
    'trigger': 'lock',
    'source': 'unlocked',
    'target': 'locked',
    'effect': 'lock()'
}

t3 = {
    'trigger': 'unlock',
    'source': 'unlocked',
    'target': 'unlocked',
}


def getWeatherTransitions():
    return [t0, t1, t2, t3]

class WeatherLock:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.stm = None
        self.mqtt_client = MQTTClient()
        self.controller = MainController()


    def unlock(self):
        self._logger.info("Unlocking the scooter")
        topic = f"escooter/command/{self.controller.get_scooter_id()}"
        #self.mqtt_client.publish(topic, "unlocked")
        self.controller.unlock()

    def lock(self):
        self._logger.info("Locking the scooter")
        topic = f"escooter/command/{self.controller.get_scooter_id()}"
        #self.mqtt_client.publish(topic, "locked")
        self.controller.lock()

    
