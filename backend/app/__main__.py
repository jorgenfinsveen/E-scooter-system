import os
import time
import logging
import asyncio
import uvicorn
import argparse
from pathlib import Path
from threading import Thread
from dotenv import load_dotenv
from colorlog import ColoredFormatter 


from api.http import *
from api.mqtt import *
from api import database



DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')
#ENV = ".env.prod" if DEPLOYMENT_MODE == 'PROD' else ".env.test"
ENV = ".env.test"
ENV_PATH = Path(__file__).resolve().parent / ENV
load_dotenv(ENV_PATH)

APP_VERSION     = os.getenv("APP_VERSION", "0.1-SNAPSHOT")
APP_NAME        = os.getenv("APP_NAME", "Scooter Backend")
APP_AUTHORS     = os.getenv("APP_AUTHORS", "Backend for scooter rental system")
DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')
DISABLE_MQTT    = os.getenv("DISABLE_MQTT", "False").lower() == "true"
HTTP_HOST = None
MQTT_HOST = None
HTTP_PORT = None
MQTT_PORT = None
MQTT_TOPIC_INPUT  = None
MQTT_TOPIC_OUTPUT = None

parser = argparse.ArgumentParser(description="Start e-scooter client.")
parser.add_argument("--host", type=str, default="cm5.local", help="Server host (default: cm5.local)")


# Database configuration
# The configuration is set in the environment variables.
DB_CONFIG = {
    'host':     os.getenv('DB_HOST', 'localhost'),
    'user':     os.getenv('DB_USER', 'user'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'database'),
    'port':     3306,
}


# Checks wether to use the production or test environment
# and sets the environment variables accordingly.
# The environment variables are set in the .env file.
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




# Sets the logging format and colors
formatter = ColoredFormatter(
    "%(log_color)s[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d in %(funcName)s()] %(message)s",
    datefmt="%H:%M:%S",
    log_colors={
        'DEBUG':    'green',
        'INFO':     'cyan',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
)



def start_http_server():
    """
    Starts the HTTP server using uvicorn.
    The server is started in a separate thread.
    """
    asyncio.set_event_loop(asyncio.new_event_loop()) 
    uvicorn.run("api.http:app", host='0.0.0.0', port=HTTP_PORT, reload=False, loop="asyncio")



def start_mqtt_client():
    """
    Starts the MQTT client.
    The client is started in a separate thread.
    Will not do anything if DISABLE_MQTT is set to True.
    """
    if not DISABLE_MQTT:
        topics = {
            "input":  MQTT_TOPIC_INPUT,
            "output": MQTT_TOPIC_OUTPUT
        }
        client = mqtt_client(id=1000, host=MQTT_HOST, port=MQTT_PORT, topics=topics)
        set_mqtt_client(client)


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.stop()



def test_db(db):
    """
    Test the database connection and functionality.
    """
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
    """
    Starts the database client.
    The client is started in a separate thread.
    """
    db = database.db(DB_CONFIG)
    set_db_client(db)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        db.close()


def setup_logging():
    """
    Sets up the logging configuration.
    The logging configuration is set to use the ColoredFormatter
    and the logging level is set to DEBUG for development mode
    and INFO for production mode.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger()

    if DEPLOYMENT_MODE == 'PROD':
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    return logger


def get_host_ip():
    args = parser.parse_args()
    return args.host


if __name__ == "__main__":
    """
    Main function and entry point to start the application.
    It starts the HTTP server, MQTT client and database client
    in separate threads.
    """
    global mqtt_thread
    global http_thread
    global db_thread

    ip_address = get_host_ip()
    logger = setup_logging()

    logger.info(f"Starting {APP_NAME}")
    logger.info(55*"-")
    logger.info(f"{APP_AUTHORS}\n")
    logger.warning(f"App version: \t{APP_VERSION}")
    logger.warning(f"Deployment mode: \t{DEPLOYMENT_MODE}\n")

    logger.info(f"Launching HTTP Server: \t{ip_address}:{HTTP_PORT}")
    http_thread = Thread(target=start_http_server)
    http_thread.start()

    
    logger.info(f"Launching MQTT Server: \t{ip_address}:{MQTT_PORT}")
    mqtt_thread = Thread(target=start_mqtt_client)
    mqtt_thread.start()

    logger.info(f"Connecting to DB: \t\t{DB_CONFIG['host']}:{DB_CONFIG['port']}\n")
    db_thread = Thread(target=start_db_client)
    db_thread.start()
    

    
