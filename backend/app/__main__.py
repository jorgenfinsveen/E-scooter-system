import os
import asyncio
import uvicorn
from app.api.http import *
from app.api.mqtt import *
from app.logic import *
from threading import Thread

DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')
DISABLE_MQTT    = bool(os.getenv('DISABLE_MQTT', True))
HTTP_HOST = None
MQTT_HOST = None
HTTP_PORT = None
MQTT_PORT = None
MQTT_TOPIC_INPUT  = None
MQTT_TOPIC_OUTPUT = None



if DEPLOYMENT_MODE == 'PROD':
    HTTP_HOST = os.getenv('HTTP_HOST_PROD', 'localhost')
    MQTT_HOST = os.getenv('MQTT_HOST_PROD', 'localhost')

    HTTP_PORT = int(os.getenv('HTTP_PORT_PROD', 8080))
    MQTT_PORT = int(os.getenv('MQTT_PORT_PROD', 1883))

    MQTT_TOPIC_INPUT  = os.getenv('MQTT_TOPIC_INPUT_PROD',  'ttm4115/team_16/request')
    MQTT_TOPIC_OUTPUT = os.getenv('MQTT_TOPIC_OUTPUT_PROD', 'ttm4115/team_16/response')
else:
    HTTP_HOST = os.getenv('HTTP_HOST_TEST', 'localhost')
    MQTT_HOST = os.getenv('MQTT_HOST_TEST', 'localhost')

    HTTP_PORT = int(os.getenv('HTTP_PORT_TEST', 8080))
    MQTT_PORT = int(os.getenv('MQTT_PORT_TEST', 1883))

    MQTT_TOPIC_INPUT  = os.getenv('MQTT_TOPIC_INPUT_TEST',  'ttm4115/team_16/request')
    MQTT_TOPIC_OUTPUT = os.getenv('MQTT_TOPIC_OUTPUT_TEST', 'ttm4115/team_16/response')



def start_http_server():
    asyncio.set_event_loop(asyncio.new_event_loop()) 
    uvicorn.run("app.api.http:app", host='0.0.0.0', port=HTTP_PORT, reload=False, loop="asyncio")

def start_mqtt_client():
    if not DISABLE_MQTT:
        topics = {
            "input":  MQTT_TOPIC_INPUT,
            "output": MQTT_TOPIC_OUTPUT
        }
        mqtt_client = MqttClient(id=1000, host=MQTT_HOST, port=MQTT_PORT, topics=topics)
        set_mqtt_client(mqtt_client)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.stop()


if __name__ == "__main__":
    global mqtt_thread
    global http_thread

    mqtt_thread = Thread(target=start_mqtt_client)
    http_thread = Thread(target=start_http_server)


    mqtt_thread.start()
    http_thread.start()
