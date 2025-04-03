from stmpy import Machine, Driver
import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, crash_detection):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.crash_detection = crash_detection  

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker:", mqtt.connack_string(rc))
        client.subscribe("escooter/crash")
        client.subscribe("escooter/safe")

    #Litt usikker på om denne trengs
    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"MQTT message received: {msg.topic}")

        if payload == "crash":
            self.crash_detection.stm.send("crash")
        elif payload == "safe":
            self.crash_detection.stm.send("safe")

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def start(self, broker, port=1883):
        self.client.connect(broker, port)
        self.client.loop_start()  

class CrashDetection:
    def __init__(self):
        self.stm = None
        self.mqtt_client = MQTTClient()

    def alarm_on(self):
        print("Alarm activated")
        self.mqtt_client.publish("escooter/alarm", "on")

    def alarm_off(self):
        print("Alarm deactivated")
        self.mqtt_client.publish("escooter/alarm", "off")

    def send_distress(self):
        print("Sending distress signal")
        self.stm.send("crash")
        self.mqtt_client.publish("escooter/distress", "sent")

    def stop_distress(self):
        print("Stopping distress signal")
        self.stm.send("safe")
        self.mqtt_client.publish("escooter/distress", "stopped")


t0 = {
    'source': 'initial',
    'target': 'standby',
}

t1 = {
    'trigger': 'crash',
    'source': 'standby',
    'target': 'crash_detected',
    'effect': 'start_timer("t", 60)'
}

t2 = {
    'trigger': 'safe',
    'source': 'crash_detected',
    'target': 'standby',
    'effect': 'stop_timer("t")'
}

t3 = {
    'trigger': 't',
    'source': 'crash_detected',
    'target': 'distress',
    'effect': 'send_distress(); alarm_on()'
}

t4 = {
    'trigger': 'safe',
    'source': 'distress',
    'target': 'standby',
    'effect': 'stop_distress(); alarm_off()'
}
 
escooter = CrashDetection()
mqtt_client = MQTTClient(escooter)  
machine = Machine(name="escooter", transitions=[t0, t1, t2, t3, t4], obj=escooter)
escooter.stm = machine


driver = Driver()
driver.add_machine(machine)
driver.start()