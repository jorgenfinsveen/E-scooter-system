from stmpy import Machine, Driver
import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, weather_lock):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.weather_lock = weather_lock  

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker:", mqtt.connack_string(rc))
        client.subscribe("escooter/unlock")
        client.subscribe("escooter/lock")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"MQTT message received: {msg.topic}")

        if payload == "unlock":
            self.weather_lock.stm.send("unlock")
        elif payload == "lock":
            self.weather_lock.stm.send("lock")

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def start(self, broker, port=1883):
        self.client.connect(broker, port)
        self.client.loop_start()  


class WeatherLock:
    def __init__(self):
        self.stm = None
        self.mqtt_client = MQTTClient()

    def unlock(self):
        print("Unlocking the scooter")
        self.mqtt_client.publish("escooter/status", "unlocked")
        self.stm.send("unlock")

    def lock(self):
        print("Locking the scooter")
        self.stm.send("lock")
        self.mqtt_client.publish("escooter/status", "locked")


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
