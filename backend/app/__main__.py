import os
import logging
import asyncio
import uvicorn
from app.api.http import *
from app.api.mqtt import *
from app.logic import *
from threading import Thread

APP_VERSION     = os.getenv("APP_VERSION", "0.1-SNAPSHOT")
DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')
DISABLE_MQTT    = os.getenv("DISABLE_MQTT", "False").lower() == "true"
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

    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
else:
    HTTP_HOST = os.getenv('HTTP_HOST_TEST', 'localhost')
    MQTT_HOST = os.getenv('MQTT_HOST_TEST', 'localhost')

    HTTP_PORT = int(os.getenv('HTTP_PORT_TEST', 8080))
    MQTT_PORT = int(os.getenv('MQTT_PORT_TEST', 1883))

    MQTT_TOPIC_INPUT  = os.getenv('MQTT_TOPIC_INPUT_TEST',  'ttm4115/team_16/request')
    MQTT_TOPIC_OUTPUT = os.getenv('MQTT_TOPIC_OUTPUT_TEST', 'ttm4115/team_16/response')

    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )



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

    logger = logging.getLogger(__name__)
    logger.info("Starting application...")
    logger.info(f"App version: {APP_VERSION}")
    logger.info(f"Deployment mode: {DEPLOYMENT_MODE}")
    logger.info(f"Launching HTTP Server: {HTTP_HOST}:{HTTP_PORT}")
    logger.info(f"Launching MQTT Server: {MQTT_HOST}:{MQTT_PORT}")
    mqtt_thread = Thread(target=start_mqtt_client)
    http_thread = Thread(target=start_http_server)


    mqtt_thread.start()
    http_thread.start()
