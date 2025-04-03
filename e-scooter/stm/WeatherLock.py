from stmpy import Machine, Driver
from api.mqtt import MQTTClient


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


    def unlock(self):
        print("Unlocking the scooter")
        self.mqtt_client.publish("escooter/status", "unlocked")
        #self.stm.send("unlock")

    def lock(self):
        print("Locking the scooter")
        self.stm.send("lock")
        #self.mqtt_client.publish("escooter/status", "locked")

    



"""
escooter = WeatherLock()
mqtt_client = MQTTClient(weather_lock=escooter)

machine = Machine(name="escooter", transitions=[t0, t1, t2, t3], obj=escooter)
escooter.stm = machine

driver = Driver()
driver.add_machine(machine)

mqtt_client.weather_lock = escooter

driver.start()
# TODO: Add broker name 
mqtt_client.start("broker_name", 1883) 
"""
