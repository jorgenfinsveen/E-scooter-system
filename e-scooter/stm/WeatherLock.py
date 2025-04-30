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
        self.stm = None
        self.mqtt_client = MQTTClient()
        self.controller = MainController()


    def unlock(self):
        print("Unlocking the scooter")
        self.mqtt_client.publish("escooter/status", "unlocked")
        self.controller.unlock()

    def lock(self):
        print("Locking the scooter")
        self.mqtt_client.publish("escooter/status", "locked")
        self.controller.lock()

    
