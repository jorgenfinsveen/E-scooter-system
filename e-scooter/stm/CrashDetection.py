from stmpy import Machine, Driver
from api.mqtt import MQTTClient


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
    'effect': 'send_distress(); alarm_on();'
}

t4 = {
    'trigger': 'safe',
    'source': 'distress',
    'target': 'standby',
    'effect': 'stop_distress(); alarm_off()'
}



def getCrashTransitions():
    return [t0, t1, t2, t3, t4]

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

