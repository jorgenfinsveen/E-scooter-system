import logging

from api.mqtt import MQTTClient
from controller.MainController import MainController

# Transitions
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
    """
    Returns the state machine transitions for the crash detection.
    """
    return [t0, t1, t2, t3]

class CrashDetection:
    """
    The CrashDetection class manages the state machine for crash detection.
    It sends a distress signal if a crash is detected and the user is not safe.
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.stm = None
        self.mqtt_client = MQTTClient()
        self.controller = MainController()

    def report_crash(self):
        """
        Report a crash by logging it to the console.
        """
        self._logger.warning("Crash detected: Sending distress signal in 10 seconds.")
    
    def user_safe(self):
        """
        Report that the user is safe by logging to the console.
        """
        self._logger.warning("User is safe: Stopping distress signal.")
    
    def send_distress(self):
        """
        Send a distress signal and aborting the session. Also locks the scooter.
        """
        self._logger.warning("Sending distress signal")
        self.mqtt_client.abort_session(cause="distress")
        self.controller.lock()
