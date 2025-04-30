import logging
from api.mqtt import MQTTClient
from controller.MainController import MainController

t0 = {
    'source': 'initial',
    'target': 'standby'
}

t1 = {
    'source':  'standby',
    'target':  'crash_detected',
    'effect':  'start_timer("t", 10_000); report_crash()',
    'trigger': 'crash'
}

t2 = {
    'source':  'crash_detected',
    'target':  'standby',
    'effect':  'stop_timer("t"); user_safe()',
    'trigger': 'safe'
}

t3 = {
    'source':  'crash_detected',
    'target':  'distress',
    'effect':  'send_distress()',
    'trigger': 't'
}


def getCrashTransitions():
    return [t0, t1, t2, t3]

class CrashDetection:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.stm = None
        self.mqtt_client = MQTTClient()
        self.controller = MainController()

    def report_crash(self):
        self._logger.warning("Crash detected: Sending distress signal in 10 seconds.")
    
    def user_safe(self):
        self._logger.info("User is safe: Stopping distress signal.")
    
    def send_distress(self):
        self._logger.warning("Sending distress signal")
        self.mqtt_client.abort_session(cause="distress")
        self.controller.lock()
