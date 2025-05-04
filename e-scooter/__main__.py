import logging
import argparse
from colorlog import ColoredFormatter 

from api.mqtt import MQTTClient
from controller.SenseHAT import SenseHAT
from tools.initializer import Initializer
from controller.MainController import MainController


parser = argparse.ArgumentParser(description="Start e-scooter client.")
parser.add_argument("--id",   type=int, default=1,             help="Scooter ID (must be positive integer)")
parser.add_argument("--host", type=str, default="192.168.10.247", help="MQTT broker host (default: 192.168.10.247)")
parser.add_argument("--port", type=int, default=1885,          help="MQTT broker port (default: 1885)")
args = parser.parse_args()

if args.id <= 0:
    print("Error: Scooter ID must be a positive integer.")
    exit(1)

HOST = str(args.host)
PORT = int(args.port)
SCOOTER_ID = args.id
LOGGER_LEVEL = logging.DEBUG
MQTT_INPUT_TOPIC = f"escooter/command/{SCOOTER_ID}"
MQTT_OUTPUT_TOPIC = f"escooter/response/{SCOOTER_ID}"

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

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger()

    logger.setLevel(LOGGER_LEVEL)
    logger.addHandler(handler)
    
    return logger

if __name__ == "__main__":
    logger = setup_logging()
    logger.info(f"Starting scooter with id: {SCOOTER_ID}")

    main_controller = MainController(SCOOTER_ID)
    initializer     = Initializer(main_controller)

    logger.info(f"MQTT:")
    logger.info(f"\tHost:\t {HOST}:{PORT}")
    mqtt_client = MQTTClient(host=HOST, port=PORT, controller=main_controller)
    mqtt_client.subscribe(MQTT_INPUT_TOPIC)
    logger.info(f"\tConnected:\t {mqtt_client.is_connected()}")

    main_controller.set_mqtt_client(mqtt_client)
    initializer.init_driver() 

    senseHat = SenseHAT()
    main_controller.setSense(senseHat)
    senseHat.set_controller(main_controller)
