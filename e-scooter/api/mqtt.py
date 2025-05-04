import sys
import time
import json
import logging
import paho.mqtt.client as mqtt

from tools.singleton import singleton


@singleton
class MQTTClient:
    def __init__(self, host=None, port=None, controller=None):
        self._logger = logging.getLogger(__name__)
        if controller != None:
            self.controller = controller

        if (host!=None and port!=None):
            self.client = mqtt.Client()
            self._start(host, port)


    def _start(self, host, port):
        try:
            self.client.connect(host, port)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.loop_start()

            return self.client
        except Exception as e:
            self._logger.error("Error in MQTT")
            sys.exit(1)

    def is_connected(self):
        try:
            return self.client.is_connected()
        except Exception as e:
            sys.exit(1)

    def on_connect(self, client, userdata, flags, rc):
        self._logger.debug(f"Connected to MQTT Broker: {mqtt.connack_string(rc)}")

    def on_message(self, client, userdata, msg):
        payload_str = msg.payload.decode()
        payload = json.loads(payload_str)

        self._server_id = payload["id"]
        self._scooter_id = payload["uuid"]
        self._command = payload["command"]
        self._coride = payload["coride"]


        if self._command == "unlock":
            response = self._build_response()
            self.publish(f"escooter/response/{self._scooter_id}", response)
            self.controller.unlock()
        elif self._command == "lock":
            response = self._build_response()
            self.publish(f"escooter/response/{self._scooter_id}", response)
            if not self.controller.is_locked():
                self.controller.lock()
        else:
            self._logger.error("Unknown command received:", self._command)
        

    def _build_response(self):
        response = {
            "id": self._server_id,
            "uuid": self._scooter_id,
            "battery": 100,
            "status": 0,
            "abort": False,
            "timestamp": time.time(),
            "location": {
                "latitude":  63.4197,
                "longitude": 10.4018
            }
        }
        return response
        
    def publish(self, topic, message):
        self.client.publish(topic, json.dumps(message)) 

    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.client.on_message = self.on_message
        self.client.loop_start()

    def abort_session(self, cause="unknown"):
        if cause == "weather":
            status = 2
        elif cause == "distress":
            status = 4
        else:
            status = 7
        
        message = {
            "id": self._server_id,
            "uuid": self._scooter_id,
            "battery": 100,
            "status": status,
            "abort": True,
            "timestamp": time.time(),
            "location": {
                "latitude":  63.4197,
                "longitude": 10.4018
            }
        }

        self.publish(f"escooter/response/{self._scooter_id}", message)
        