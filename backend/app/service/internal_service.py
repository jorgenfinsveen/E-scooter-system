import os
import json
import time
import logging
from datetime import datetime

from api import database
from logic import transaction
from tools.singleton import singleton


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOOTER_STATUS_CODES_PATH = os.path.join(BASE_DIR, "resources/scooter-status-codes.json")
DISABLE_MQTT    = os.getenv("DISABLE_MQTT", "False").lower() == "true"

@singleton
class internal_service:
    """
    This class handles the internal service for server-related events.
    It is responsible for handling session aborts.
    """
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._db = database.db()
        with open(SCOOTER_STATUS_CODES_PATH, 'r') as f:
            self._status_codes = json.load(f)


    def session_aborted(self, scooter_id: int, payload: dict) -> tuple[bool, bool]:
        """
        Handle the session aborted event.
        This function is called when the scooter session is aborted.
        It updates the scooter status in the database and charges the user for the ride.
        Args:
            scooter_id (int): The ID of the scooter.
            payload (dict): The payload data from the scooter upon abort alert.
        """
        self._logger.warning(f"Session aborted for scooter {scooter_id}: {self._status_codes[str(payload['status'])]}")

        rental = self._parse_rental(self._db.get_active_rental_by_scooter(scooter_id))
        user   = self._parse_user(self._db.get_user(rental['user_id']))
        self._handle_abort_cause(payload['status'], user, rental, scooter_id, payload['location']['latitude'], payload['location']['longitude'])

        time_s = rental['start_time'].timestamp()
        time_e = datetime.fromtimestamp(time.time()).timestamp()
        time_d = abs((time_e - time_s) / 60.0)

        _, _, price        = transaction.pay_for_single_ride(user, time_d)
        db_req_payment     = self._db.charge_user(user['id'], price)
        db_rental_complete = self._db.rental_completed(user['id'], price, 
                                  payload['location']['latitude'], 
                                  payload['location']['longitude'], 
                                  payload['status'])
        
        return db_rental_complete, db_req_payment
    



    def _handle_abort_cause(self, status: int, user: dict, rental: dict, scooter: int, lat: float, lon: float) -> None:
        """
        Handle the cause of the session abort.
        This function is called when the scooter session is aborted.
        If the abort is due to distress, it will log the event and contact emergency services.
        Args:
            status (int): The status code of the scooter.
            user (dict): The user data from the database.
            rental (dict): The rental data from the database.
            scooter (int): The ID of the scooter.
            lat (float): The latitude of the scooter location.
            lon (float): The longitude of the scooter location.
        """
        if self._status_codes[str(status)] == "distress":
            self._logger.critical("Session aborted due to distress alert:")
            self._logger.critical(f"\tUser: {user['name']}")
            self._logger.critical(f"\tScooter: {scooter}")
            self._logger.critical(f"\tTime: {datetime.fromtimestamp(time.time())}")
            self._logger.critical(f"\tLocation:")
            self._logger.critical(f"\t\tLatitude:  {lat}")
            self._logger.critical(f"\t\tLongitude: {lon}")
            self._logger.critical(f"Contacting emergency services...")



    def _parse_rental(self, rental: dict) -> dict:
        """
        Parse the rental data from the database.
        
        Args:
            rental (dict): The rental data from the database.
        
        Returns:
            dict: The parsed rental data.

        Example:
        ```python
            _rental  = self._db.get_active_rental_by_user(user_id)
            self._parse_rental(_rental) -> {
                "rental_id": 4,
                "user_id": 1,
                "scooter_id": 7,
                "active": True,
                "start_time": datetime('2025-03-31 11:25:29'),
                "end_time": time.time(),
                "price": 65.4
            }
        ```
        """
        return {
            "rental_id": rental[0],
            "user_id": rental[1],
            "scooter_id": rental[2],
            "active": rental[3],
            "start_time": rental[4],
            "end_time": time.time(),
            "price": rental[6]
        }
    


    def _parse_user(self, user: dict) -> dict:
        """
        Parse the user data from the database.
        
        Args:
            user (dict): The user data from the database.
        
        Returns:
            dict: The parsed user data.

        Example:
        ```python
            _user = self._db.get_user(user_id)
            self._parse_user(_user) -> {
                "id": 1, 
                "name": John Doe,
                "funds": 350.0
            }
        ```
        """
        return {
            "id": user[0],
            "name": user[1],
            "funds": user[2]
        }
