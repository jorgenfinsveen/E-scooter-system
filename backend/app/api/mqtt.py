import sys
import os
import paho.mqtt.client as mqtt
import stmpy
from threading import Thread
from threading import Event
import json
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOOTER_STATUS_CODES_PATH = os.path.join(BASE_DIR, "scooter-status-codes.json")


class MqttClient:

    def __init__(self : object, id : int, host : str, port : int, topics: dict) -> None:
        self._id = id
        self._status = 'disconnected'
        self._response_event = Event()
        self._client = self._init_client(host, port, topics)
        self.output_topic = topics["output"]
        self._message = None
        with open(SCOOTER_STATUS_CODES_PATH, 'r') as f:
            self._status_codes = json.load(f)

    def _init_client(self : object, host : str, port : int, topics : dict) -> mqtt.Client:
        try:
            self._client = mqtt.Client()
            self._client.connect(host, port)
            self._client.subscribe(topics["input"])
            self._client.on_connect = self.on_connect
            self._client.on_message = self.on_message
            self._client.loop_start()

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        return self._client

    def on_connect(self : object, client : mqtt.Client) -> None:
        self._status = 'connected'

    def on_message(self : object, client : mqtt.Client, userdata : object, msg : dict) -> None:
        message = json.loads(msg.payload)
        print(f"Message received: {message}")
        self._message = message

        if message.get("command") == "unlock_ack":  
            self._response_event.set()

    def stop(self : object) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    def send_message(self : object, message : dict) -> None:
        self._client.publish(self.output_topic, json.dumps(message))

    def location_is_valid(self : object, location : str) -> bool:
        return True

    def scooter_unlock_single(self : object, uuid : str) -> tuple[bool, str]:
        self._response_event.clear()

        message = {
            "id": self._id,
            "uuid": uuid,
            "command": "unlock",
            "coride": False,
            "num_coriders": 0,
            "coriders": [],
            "timestamp": time.time()
        }

        self.send_message(message)

        response = self._response_event.wait(timeout=15)

        if response:
            try:
                if self._message['_id'] == self._id and self._message['uuid'] == uuid:
                    battery   = int(self._message['battery'])
                    status    = int(self._message['status'])
                    location  = str(self._message['location'])
                    timestamp = self._message['timestamp']

                    if battery > 15 and status == 0:
                        return True, "Unlock successful"
                    elif battery <= 15:
                        return False, "Battery too low"
                    elif status > 0:
                        return False, self._status_codes[str(status)]
            except Exception as e:
                return False, f"Error parsing lock confirmation: {e}"
        else:
            return False, "Timeout waiting for unlock confirmation"



    def scooter_lock_single(self : object, uuid : str) -> tuple[bool, str]:
        self._response_event.clear()  

        message = {
            "id": self._id,
            "uuid": uuid,
            "command": "lock",
            "coride": False,
            "num_coriders": 0,
            "coriders": [],
            "timestamp": time.time()
        }

        self.send_message(message)

        response = self._response_event.wait(timeout=30)

        if response:
            try:
                if self._message['_id'] == self._id and self._message['uuid'] == uuid:
                    battery   = int(self._message['battery'])
                    status    = int(self._message['status'])
                    location  = str(self._message['location'])
                    timestamp = self._message['timestamp']

                    if status == 0 and self.location_is_valid(location):
                        return True, "Lock successful"
                    elif not self.location_is_valid(location):
                        return False, "Invalid parking location"
                    elif status > 0:
                        return False, self._status_codes[str(status)]
            except Exception as e:
                return False, f"Error parsing lock confirmation: {e}"
        else:
            return False, "Timeout waiting for lock confirmation"

