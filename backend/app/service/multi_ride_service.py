import logging
from app.api import mqtt
from app.logic import weather
from app.logic import database
from app.logic import transaction
from app.tools.singleton import singleton



@singleton
class multi_ride_service:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._db = database.db()
        self._mqtt = mqtt.mqtt_client()
