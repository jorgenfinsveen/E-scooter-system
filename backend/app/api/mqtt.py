import os
import sys
import json
import time
import logging
from threading import Event
import paho.mqtt.client as mqtt

from tools.singleton import singleton
from service.internal_service import internal_service


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOOTER_STATUS_CODES_PATH = os.path.join(BASE_DIR, "resources/scooter-status-codes.json")
DISABLE_MQTT    = os.getenv("DISABLE_MQTT", "False").lower() == "true"
DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')


if DEPLOYMENT_MODE == 'PROD':
    MQTT_HOST = os.getenv('MQTT_HOST_PROD', 'localhost')
    MQTT_PORT = int(os.getenv('MQTT_PORT_PROD', 1883))
    MQTT_TOPIC_INPUT  = os.getenv('MQTT_TOPIC_INPUT_PROD',  'ttm4115/team_16/request')
    MQTT_TOPIC_OUTPUT = os.getenv('MQTT_TOPIC_OUTPUT_PROD', 'ttm4115/team_16/response')

else:
    MQTT_HOST = os.getenv('MQTT_HOST_TEST', 'localhost')
    MQTT_PORT = int(os.getenv('MQTT_PORT_TEST', 1883))
    MQTT_TOPIC_INPUT  = os.getenv('MQTT_TOPIC_INPUT_TEST',  'ttm4115/team_16/request')
    MQTT_TOPIC_OUTPUT = os.getenv('MQTT_TOPIC_OUTPUT_TEST', 'ttm4115/team_16/response')


@singleton
class mqtt_client:
    """
    MQTT client for scooter rental system.
    This class handles the connection to the MQTT broker, subscribes to topics,
    and publishes messages to the broker.
    This class is a singleton, meaning only one instance of it can exist at a time.

    On first initialization, parameters must be provided.
    After that, the same instance will be used throughout the application meaning
    that one do not need to provide parameters again.

    #### Example:
    ```python
    from app.api.mqtt import MqttClient

    topics = {
        "input":  "test/input_topic",
        "output": "test/output_topic"
    }

    mqtt1 = mqtt.mqtt(host="localhost", port=1883, topics=topics)
    mqtt2 = mqtt.mqtt(host=None, port=None, topics=None)

    assert mqtt1 is mqtt2  # True, both variables point to the same instance.
    ```
    """

    def __init__(self : object, id : int=None, host: str=None, port: int=None, topics: dict=None) -> None:
        """
        Initialize the MQTT client.
        If the parameters are not provided, it will use the existing instance.
        Args:
            id (int): ID of the the MQTT broker.
            host (str): Hostname of the MQTT broker.
            port (int): Port of the MQTT broker.
            topics (dict): Dictionary containing the input and output topics.
        Example:
            ```python
            from app.api.mqtt import MqttClient

            topics = {
                "input":  "test/input_topic",
                "output": "test/output_topic"
            }

            mqtt = mqtt.mqtt(host="localhost", port=1883, topics=topics)
            ```
        """
        if DISABLE_MQTT:
            return
        self._logger = logging.getLogger(__name__)
        self._id = id
        self._status = 'disconnected'
        self._response_event = Event()
        self.input_topic  = MQTT_TOPIC_INPUT
        self.output_topic = MQTT_TOPIC_OUTPUT
        self._client = self._init_client(MQTT_HOST, MQTT_PORT)
        self._internal_service = internal_service()
        self._message = None
        with open(SCOOTER_STATUS_CODES_PATH, 'r') as f:
            self._status_codes = json.load(f)



    def _init_client(self : object, host : str, port : int) -> mqtt.Client:
        """
        Internal function to initialize the actual MQTT client object.
        Args:
            host (str): Hostname of the MQTT broker.
            port (int): Port of the MQTT broker.
            topics (dict): Dictionary containing the input and output topics.
        Returns:
            mqtt.Client: The initialized MQTT client.
        """
        try:
            self._client = mqtt.Client()
            self._client.connect(host, port)
            self._client.subscribe(self.input_topic)
            self._client.on_connect = self.on_connect
            self._client.on_message = self.on_message
            self._client.loop_start()

        except Exception as e:
            self._logger.critical(f"Could not connect to host: {e}")
            sys.exit(1)

        return self._client


    def on_connect(self, client, userdata, flags, rc) -> None:
        """
        Callback function for when the client connects to the broker.
        This function is called when the client connects to the broker.
        It sets the status to 'connected' and logs the connection.
        Args:
            client (mqtt.Client): The MQTT client instance.
        """
        self._status = 'connected'
        self._logger.info(f"Connected to MQTT broker at {client._host}:{client._port}")



    def on_message(self, client, userdata, msg) -> None:
        """
        Callback function for when a message is received from the broker.
        This function is called when a message is received from the broker.
        It logs the message and sets the response event.
        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata (object): User data passed to the callback.
            msg (dict): The message received from the broker.
        """
        payload_str = msg.payload.decode()
        message = json.loads(payload_str)
        self._logger.info(f"At {self.input_topic} - received message: {message}")

        if message["abort"] == True:
            self._internal_service.session_aborted(message["uuid"], message)
        else:
            self._message = message
            self._response_event.set()



    def stop(self : object) -> None:
        """
        Stop the MQTT client.
        This function stops the MQTT client and disconnects from the broker.
        It sets the status to 'disconnected' and logs the disconnection.
        """
        self._client.loop_stop()
        self._client.disconnect()
        self._logger.info("Disconnected from MQTT broker")



    def send_message(self : object, message : dict) -> None:
        """
        Send a message to the MQTT broker.
        This function sends a message to the MQTT broker.
        Args:
            message (dict): The message to send.
        """
        topic = f"{self.output_topic}/{message['uuid']}"
        self._client.publish(topic, json.dumps(message))
        self._logger.info(f"At {topic} - published message: {message}")



    def location_is_valid(self : object, location : dict) -> bool:
        """
        Check if the location is valid.
        This function checks if the location is valid.
        Args:
            location (str): The location to check.
        Returns:
            bool: True if the location is valid, False otherwise.
        
        Example:
        ```python
            mqtt.location_is_valid({63.41947, 10.40174}) -> True
        ```
        """
        return True


    # TODO: These needs to receive the whole scooter object. Needs to check if scooter is already locked/unlocked
    def scooter_unlock_single(self : object, scooter : dict) -> tuple[bool, int, str]:
        """
        This function unlocks a scooter.
        Args:
            scooter (dict): The scooter to unlock.
        Returns:
            tuple: 
             * [0]: _bool_. True if the unlock was successful, False otherwise.
             * [1]: _str_. A message indicating the result of the unlock operation.
        Example:
            ```python
                mqtt.scooter_unlock_single("1234") -> (True, "unlock successful")
                mqtt.scooter_unlock_single("1235") -> (False, "battery too low")
            ```
        """
        self._response_event.clear()

        if scooter['status'] == 11:
            return False, 11, "scooter-occupied"

        message = {
            "id": self._id,
            "uuid": scooter['uuid'],
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
                if int(self._message['id']) == int(self._id) and str(self._message['uuid']) == str(scooter['uuid']):
                    battery   = int(self._message['battery'])
                    status    = int(self._message['status'])
                    # location  = str(self._message['location'])
                    # timestamp = self._message['timestamp']

                    if battery > 15 and status == 0:
                        return True, status, ""
                    elif battery <= 15:
                        return False, status, "low-battery"
                    elif status > 0:
                        return False, status, "scooter-inoperable"
            except Exception as e:
                self._logger.error(f"Exception while parsing unlock response: {e}")
                self._logger.error(f"Message content: {self._message}")
                return False, 7, "scooter-inoperable"
        else:
            self._logger.error("Did not get response")
            return False, 7, "scooter-inoperable"




    def scooter_lock_single(self : object, scooter : dict) -> tuple[bool, str, int]:
        """
        This function locks a scooter.
        Args:
            scooter (dict): The scooter to lock.
        Returns:
            tuple: 
             * [0]: _bool_. True if the lock was successful, False otherwise.
             * [1]: _str_. A message indicating the result of the lock operation.
             * [2]: _int_. The status of the scooter.
        Example:
            ```python
                mqtt.scooter_lock_single("1234") -> (True, "lock successful")
                mqtt.scooter_lock_single("1235") -> (False, "invalid parking location")
            ```
        """
        self._response_event.clear()  

        message = {
            "id": self._id,
            "uuid": scooter["uuid"],
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
                if int(self._message['id']) == int(self._id) and str(self._message['uuid']) == str(scooter["uuid"]):
                    battery   = int(self._message['battery'])
                    status    = int(self._message['status'])
                    location  = str(self._message['location'])
                    timestamp = self._message['timestamp']

                    if status == 0 and self.location_is_valid(location):
                        return True, "lock successful", status
                    elif not self.location_is_valid(location):
                        return False, "invalid parking location", status
                    elif status > 0:
                        return False, self._status_codes[str(status)]
            except Exception as e:
                return False, f"error parsing lock confirmation: {e}", -1
        else:
            return False, "timeout waiting for lock confirmation", -1

