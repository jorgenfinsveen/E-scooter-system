import os
import logging
import asyncio
import uvicorn
from pathlib import Path
from app.api.http import *
from app.api.mqtt import *
from threading import Thread
from app.logic import database
from dotenv import load_dotenv

DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')
ENV = ".env.prod" if DEPLOYMENT_MODE == 'PROD' else ".env.test"
ENV_PATH = Path(__file__).resolve().parent / ENV
load_dotenv(ENV_PATH)

APP_VERSION     = os.getenv("APP_VERSION", "0.1-SNAPSHOT")
DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')
DISABLE_MQTT    = os.getenv("DISABLE_MQTT", "False").lower() == "true"
HTTP_HOST = None
MQTT_HOST = None
HTTP_PORT = None
MQTT_PORT = None
MQTT_TOPIC_INPUT  = None
MQTT_TOPIC_OUTPUT = None




DB_CONFIG = {
    'host':     os.getenv('DB_HOST', 'localhost'),
    'user':     os.getenv('DB_USER', 'user'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'database'),
    'port':     3306,
}



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



def test_db(db):
    db.add_user("John Doe", 350.0)
    db.add_scooter(65.41947, 12.40174, 0)
    users = db.get_all_users()
    scooters = db.get_all_scooters()

    for user in users:
        logger.debug(f"User:")
        for key, value in user.items():
            logger.debug(f"\t{key}: {value}")

    for scooter in scooters:
        logger.debug(f"Scooter:")
        for key, value in scooter.items():
            logger.debug(f"\t{key}: {value}")



def start_db_client():
    db = database.db(DB_CONFIG)
    set_db_client(db)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        db.close()



if __name__ == "__main__":
    global mqtt_thread
    global http_thread
    global db_thread

    logger = logging.getLogger(__name__)
    logger.info("Starting application...")
    logger.info(f"App version: {APP_VERSION}")
    logger.info(f"Deployment mode: {DEPLOYMENT_MODE}")
    logger.info(f"Launching HTTP Server: {HTTP_HOST}:{HTTP_PORT}")
    logger.info(f"Launching MQTT Server: {MQTT_HOST}:{MQTT_PORT}")
    logger.info(f"Connecting to DB: {DB_CONFIG['host']}:{DB_CONFIG['port']}")

    mqtt_thread = Thread(target=start_mqtt_client)
    http_thread = Thread(target=start_http_server)
    db_thread = Thread(target=start_db_client)

    mqtt_thread.start()
    http_thread.start()
    db_thread.start()
