import os
import logging
import mysql.connector



class db:
    def __init__(self, credentials) -> None:
        self._conn = None
        self._cursor = None
        self._logger = logging.getLogger(__name__)
        self._connect(credentials)



    def _connect(self: object, credentials) -> None:
        try:
            self._conn = mysql.connector.connect(**credentials)
            self._cursor = self._conn.cursor(dictionary=True)
            self._logger.info("Connected to the database")
        except mysql.connector.Error as e:
            self._logger.error(f"Error connecting to the database: {e}")
            raise



    def close(self: object) -> None:
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()



    def get_user(self: object, user_id: int) -> tuple[int, str, float]:
        query = "SELECT * FROM users WHERE id = %s"
        self._cursor.execute(query, (user_id,))
        return self._cursor.fetchone()
    


    def get_scooter(self: object, scooter_id: int) -> tuple[str, float, float, int]:
        query = "SELECT * FROM scooters WHERE id = %s"
        self._cursor.execute(query, (scooter_id,))
        return self._cursor.fetchone()
    


    def get_rental_by_id(self: object, rental_id: int) -> tuple[int, int, str, bool, str, str, float]:
        query = "SELECT * FROM rentals WHERE id = %s"
        self._cursor.execute(query, (rental_id,))
        return self._cursor.fetchone()
    


    def get_rental_by_user(self: object, user_id: int) -> tuple[int, int, str, bool, str, str, float]:
        query = "SELECT * FROM rentals WHERE user_id = %s AND is_active = 1"
        self._cursor.execute(query, (user_id,))
        return self._cursor.fetchone()
    


    def rental_started(self:object, user_id: int, scooter_id: str) -> bool:
        query = "INSERT INTO rentals (user_id, scooter_id, is_active, start_time, end_time, total_price) VALUES (%s, %s, 1, NOW(), NOW(), 0.0)"
        try:
            self._cursor.execute(query, (user_id, scooter_id))
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error starting rental: {e}")
            return False
        


    def rental_completed(self:object, user_id: int, price: float, location: dict, status: int) -> bool:
        rental = self.get_rental_by_user(user_id)
        if rental is None:
            self._logger.error("Rental not found")
            return False
        rental_id = rental["rid"]
        scooter_id = rental["scooter_id"]
        query = "UPDATE rentals SET is_active = 0, end_time = NOW(), total_price = %s WHERE user_id = %s AND scooter_id = %s AND rid = %s"
        try:
            self._cursor.execute(query, (price, user_id, scooter_id, rental_id))
            self._conn.commit()
            self._update_scooter_info(scooter_id, location, status)
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error completing rental: {e}")
            return False
        


    def _update_scooter_info(self: object, scooter_id: str, location: dict, status: int) -> bool:
        query = "UPDATE scooters SET latitude = %s, longtiude = %s, status = %s WHERE id = %s"
        try:
            self._cursor.execute(query, (location, status, scooter_id))
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error updating scooter info: {e}")
            return False
        


    def get_all_scooters(self: object) -> list:
        query = "SELECT * FROM scooters"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    


    def get_all_users(self: object) -> list:
        query = "SELECT * FROM users"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    


    def get_all_rentals(self: object) -> list:
        query = "SELECT * FROM rentals"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    


    def delete_inactive_rentals(self: object) -> bool:
        query = "DELETE FROM rentals WHERE is_active = 0"
        try:
            self._cursor.execute(query)
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error deleting inactive rentals: {e}")
            return False
        


    def get_scooter_near_location(self: object, location: dict) -> tuple[str, float, float, int]:
        query = "SELECT * FROM scooters WHERE latitude BETWEEN %s AND %s AND longtiude BETWEEN %s AND %s"
        latitude = location["latitude"]
        longitude = location["longitude"]
        self._cursor.execute(query, (latitude - 0.01, latitude + 0.01, longitude - 0.01, longitude + 0.01))
        return self._cursor.fetchall()
    


    def add_user(self: object, name: str, funds: float) -> bool:
        query = "INSERT INTO users (name, funds) VALUES (%s, %s)"
        try:
            self._cursor.execute(query, (name, funds))
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error adding user: {e}")
            return False
        


    def add_scooter(self: object, latitude: float, longitude: float, status: int) -> bool:
        query = "INSERT INTO scooters (latitude, longtitude, status) VALUES (%s, %s, %s)"
        try:
            self._cursor.execute(query, (latitude, longitude, status))
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error adding scooter: {e}")
            return False