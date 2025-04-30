import logging
from api.mqtt import MQTTClient
from controller.MainController import MainController


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
        self._logger = logging.getLogger(__name__)
        self.stm = None
        self.mqtt_client = MQTTClient()
        self.controller = MainController()

    def alarm_on(self):
        self._logger.warning("Alarm activated")
        topic = f"escooter/response/{self.controller.get_scooter_id()}"
        self.mqtt_client.publish(topic, {"message": "crash_detection_alarm_on"})


    def alarm_off(self):
        self._logger.info("Alarm deactivated")
        topic = f"escooter/response/{self.controller.get_scooter_id()}"
        self.mqtt_client.publish(topic, {"message": "crash_detection_alarm_off"})

    def send_distress(self):
        self._logger.warning("Sending distress signal")
        self.stm.send("crash")
        topic = f"escooter/response/{self.controller.get_scooter_id()}"
        self.mqtt_client.publish(topic, {"message": "distress_signal_sent"})

    def stop_distress(self):
        self._logger.info("Stopping distress signal")
        self.stm.send("safe")
        topic = f"escooter/response/{self.controller.get_scooter_id()}"
        self.mqtt_client.publish(topic, {"message": "distress_signal_stopped"})

