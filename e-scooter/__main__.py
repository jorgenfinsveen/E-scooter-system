import logging
import argparse
from api.mqtt import MQTTClient
from stm.Driver import Driver, ScooterDriver
from stm.CrashDetection import CrashDetection, getCrashTransitions
from stm.WeatherLock import WeatherLock, getWeatherTransitions
from stmpy import Machine
from controller.MainController import MainController
from controller.SenseHAT import SenseHAT
from colorlog import ColoredFormatter 

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

    logger.info(f"MQTT:")
    logger.info(f"\tHost:\t {HOST}:{PORT}")
    mqtt_client = MQTTClient(host=HOST, port=PORT, controller=main_controller)
    mqtt_client.subscribe(MQTT_INPUT_TOPIC)
    logger.info(f"\tConnected:\t {mqtt_client.is_connected()}")

    main_controller.set_mqtt_client(mqtt_client)


    driver = ScooterDriver()

    crash_detector = CrashDetection()
    crash_detector_stm = Machine(transitions=getCrashTransitions(), obj=crash_detector, name='crash_detector')
    crash_detector.stm = crash_detector_stm
    driver.add_machine(crash_detector_stm)


    weather_lock = WeatherLock()
    weather_lock_stm = Machine(transitions=getWeatherTransitions(), obj=weather_lock, name='weather_lock')
    weather_lock.stm = weather_lock_stm
    driver.add_machine(weather_lock_stm)


    senseHat = SenseHAT()
    main_controller.setDriver(driver)
    main_controller.setSense(senseHat)
    senseHat.set_controller(main_controller)




"""
driver = Driver()
driver.add_machine(machine)
driver.start()
"""
