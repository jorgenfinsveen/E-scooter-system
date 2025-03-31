import os
import time
import logging
from app.api import mqtt
from datetime import datetime
from app.logic import weather
from app.logic import database
from app.logic import transaction
from app.tools.singleton import singleton

DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'TEST')
DISABLE_MQTT    = os.getenv("DISABLE_MQTT", "False").lower() == "true"

@singleton
class single_ride_service:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._db = self.get_db_client()
        self._mqtt = self.get_mqtt_client()
        self.scooter = None
        self.user    = None



    def get_db_client(self) -> object:
        return database.db()
    


    def get_mqtt_client(self) -> object:
        return None if DISABLE_MQTT else mqtt.mqtt_client()



    def unlock_scooter(self, scooter_id: int, user_id: int) -> tuple[bool, str]:
        _scooter = self._db.get_scooter(scooter_id)
        _user = self._db.get_user(user_id)

        self.scooter = None
        self.user    = None

        if _scooter is not None:
            self.scooter = {
                "uuid": _scooter[0],
                "latitude": _scooter[1],
                "longtitude": _scooter[2],
                "status": _scooter[3]
            }
        if _user is not None:
            self.user = {
                "id": _user[0],
                "name": _user[1],
                "funds": _user[2]
            }

        user_has_active_rental = self._db.user_has_active_rental(user_id)
        sctr_has_active_rental = self._db.scooter_has_active_rental(scooter_id)

        if user_has_active_rental:
            self._logger.warning(f"User {user_id} has an active rental.")
            return False, "user has active rental"
        if sctr_has_active_rental:
            self._logger.warning(f"Scooter {scooter_id} has an active rental.")
            return False, "scooter is already rented"
        
        weather_req = weather.is_weather_ok(self.scooter["latitude"], self.scooter["longtitude"])
        balance_req = transaction.validate_funds(self.user, 100.0)


        if not weather_req[0]:
            return False, weather_req[1]
        if not balance_req[0]:
            return False, balance_req[1]

        if DISABLE_MQTT:
            mqtt_unlock = (True, "mqtt disabled", None)
        else:
            mqtt_unlock    = self._mqtt.scooter_unlock_single(self.scooter["uuid"])
        rental_started = self._db.rental_started(self.user["id"], self.scooter["uuid"])


        if mqtt_unlock[0] and rental_started:
            self._logger.info(f"Single scooter unlock successful:")
            self._logger.info(f"\tscooter-id: \t{self.scooter['uuid']}")
            self._logger.info(f"\tuser-id: \t{self.user['id']}")
            return True, "unlock successful"
        elif not mqtt_unlock[0]:
            self._logger.warning(f"Single scooter unlock failed:")
            self._logger.warning(f"\tscooter-id: \t{self.scooter['uuid']}")
            self._logger.warning(f"\tuser-id: \t{self.user['id']}")
            self._logger.warning(f"\tresponse: \t{mqtt_unlock[1]}")
            return False, mqtt_unlock[1]
        else:
            self._logger.warning(f"Single scooter unlock failed:")
            self._logger.warning(f"\tscooter-id: \t{self.scooter['uuid']}")
            self._logger.warning(f"\tuser-id: \t{self.user['id']}")
            self._logger.error(f"database error: rental not started")
            return False, "database error: rental not started"
        


    def lock_scooter(self, scooter_id: int, user_id: int) -> tuple[bool, str]:
        _scooter = self._db.get_scooter(scooter_id)
        _user    = self._db.get_user(user_id)
        _rental  = self._db.get_active_rental_by_user(user_id)

        self.scooter = None
        self.user    = None
        self.rental  = None

        if _scooter is not None:
            self.scooter = {
                "uuid": _scooter[0],
                "latitude": _scooter[1],
                "longtitude": _scooter[2],
                "status": _scooter[3]
            }
        else:
            self._logger.error(f"scooter retrieved from db.get_scooter({scooter_id}) returned None.")
            return False, "scooter not found"
        


        if _user is not None:
            self.user = {
                "id": _user[0],
                "name": _user[1],
                "funds": _user[2]
            }
        else:
            self._logger.error(f"user retrieved from db.get_user({user_id}) returned None.")
            return False, "user not found"
        

        if _rental is not None:
            self.rental = {
                "rental_id": _rental[0],
                "user_id": _rental[1],
                "scooter_id": _rental[2],
                "active": _rental[3],
                "start_time": _rental[4],
                "end_time": time.time(),
                "price": _rental[6]
            }
        else:
            self._logger.error(f"rental retrieved from db.get_active_rental_by_user({user_id}) returned None.")
            return False, "rental not found"
        
        time_start = self.rental["start_time"].timestamp()
        time_end   = datetime.fromtimestamp(time.time()).timestamp()
        time_diff  = abs((time_end - time_start) / 60.0)

        self._logger.info(f"time_diff: {time_diff}")
        self._logger.info(f"time end: {time_end}")
        self._logger.info(f"time start: {time_start}")

        if DISABLE_MQTT:
            mqtt_lock = (True, "mqtt disabled", None)
        else:
            mqtt_lock = self._mqtt.scooter_lock_single(self.scooter)
        
        price = transaction.pay_for_single_ride(self.user, time_diff)
        db_req_payment = self._db.charge_user(self.user["id"], price[2])

        if not price[0]:
            self._logger.warning(f"Single scooter lock failed - TRANSACTIONS:")
            self._logger.warning(f"\tscooter-id: \t{self.scooter['uuid']}")
            self._logger.warning(f"\tuser-id: \t{self.user['id']}")
            self._logger.warning(f"\tresponse: \t{mqtt_lock[1]}")
            self._logger.warning(f"\tprice: \t{price[2]}")
            self._logger.warning(f"\tuser-funds: \t{self.user['funds']}")
            self._logger.warning(f"\ttime: ")

            start_time_tmp = datetime.fromtimestamp(time_start)
            end_time_tmp   = datetime.fromtimestamp(time_end)
            self._logger.warning(f"\t\tstart: {time_start} \t {start_time_tmp}")
            self._logger.warning(f"\t\tend: {time_end} \t {end_time_tmp}")
            self._logger.warning(f"\t\tdiff: {time_diff}")
            return False, price[1]
        
        if not mqtt_lock[0]:
            self._logger.warning(f"Single scooter lock failed - MQTT:")
            self._logger.warning(f"\tscooter-id: \t{self.scooter['uuid']}")
            self._logger.warning(f"\tuser-id: \t{self.user['id']}")
            self._logger.warning(f"\tresponse: \t{mqtt_lock[1]}")
            return False, mqtt_lock[1]

        rental_ended = self._db.rental_completed(self.user["id"], price[2], self.scooter["latitude"], self.scooter["longtitude"], mqtt_lock[2])


        if rental_ended and db_req_payment:
            return True, mqtt_lock[1]
        elif not rental_ended:
            self._logger.warning(f"Single scooter lock failed - Database:")
            self._logger.warning(f"\tscooter-id: \t{self.scooter['uuid']}")
            self._logger.warning(f"\tuser-id: \t{self.user['id']}")
            self._logger.error(f"database error: rental not completed")
            return False, "database error: rental not completed"
        else:
            self._logger.warning(f"Single scooter lock failed - Database:")
            self._logger.warning(f"\tscooter-id: \t{self.scooter['uuid']}")
            self._logger.warning(f"\tuser-id: \t{self.user['id']}")
            self._logger.error(f"database error: payment not completed")
            return False, "database error: payment not completed"


    def _warn_logger(
            self: object, 
            title: str, 
            culprit: str=None,
            user_id: int=None,
            scooter_id: int=None,
            message: str=None,
            resp: str=None,
            time: dict=None,
            transaction: dict=None,
    ):
        """
        Log a warning message.
        
        Args:
            logger (logging.Logger): The logger to use.
            message (str): The message to log.
        """
        if culprit is not None:
            self._logger.warning(f"{title} - {culprit}")
        if user_id is not None:
            self._logger.warning(f"\tuser-id: \t{user_id}")
        if scooter_id is not None:
            self._logger.warning(f"\tscooter-id: \t{scooter_id}")
        if resp is not None:
            self._logger.warning(f"\tresponse: \t{resp}")
        if time is not None:
            start_time_tmp = datetime.fromtimestamp(time["start"])
            end_time_tmp   = datetime.fromtimestamp(time["end"])
            self._logger.warning(f"\ttime: ")
            self._logger.warning(f"\t\tstart: {time["start"]} \t {start_time_tmp}")
            self._logger.warning(f"\t\tend: {time["end"]} \t {end_time_tmp}")
            self._logger.warning(f"\t\tdiff: {time["diff"]}")
        if transaction is not None:
            self._logger.warning(f"\tprice: \t{transaction['price']}")
            self._logger.warning(f"\tuser-funds: \t{transaction['funds']}")
        if message is not None:
            self._logger.warning(f"\tmessage: \t{message}")