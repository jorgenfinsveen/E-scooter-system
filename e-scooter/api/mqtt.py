import sys
import paho.mqtt.client as mqtt
import tools.singleton as singleton

@singleton
class MQTTClient:
    def __init__(self, host=None, port=None, controller=None):
        if controller != None:
            self.controller = controller

        if (host!=None and port!=None):
            self.client = mqtt.Client()


    def _start(self, host, port):
        try:
            self.client.connect(host, port)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self._client.loop_start()

            return self.client
        except Exception as e:
            print("error in MQTT")
            sys.exit(1)


    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker:", mqtt.connack_string(rc))

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        if payload["command"] == "unlock":
            self.controller.unlock(payload)
        if payload["command"] == "lock":
            self.controller.lock(payload)
        

    def publish(self, topic, message):
        self.client.publish(topic, message) 
