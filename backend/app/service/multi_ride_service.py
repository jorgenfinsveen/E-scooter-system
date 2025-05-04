import logging

from api import mqtt, database
from tools.singleton import singleton
from logic import transaction, weather




@singleton
class multi_ride_service:
    """
    This class handles the multi-ride service for the scooter.
    It is responsible for handling the multi-ride requests and responses.
    """
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._db = database.db()
        self._mqtt = mqtt.mqtt_client()
