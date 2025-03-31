import logging
from api import mqtt
from logic import weather
from logic import database
from logic import transaction
from tools.singleton import singleton



@singleton
class multi_ride_service:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._db = database.db()
        self._mqtt = mqtt.mqtt_client()
