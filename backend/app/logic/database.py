import logging
import mysql.connector
from tools.singleton import singleton




@singleton
class db:
    """
    Database class for managing database connections and queries.
    This class is a singleton, meaning only one instance of it can exist at a time.
    It provides methods for connecting to the database, executing queries,
    and managing transactions.
    The database connection is established using the credentials provided
    during initialization.

    On first initialization, credentials must be provided.
    After that, the same instance will be used throughout the application meaning
    that one do not need to provide credentials again.

    #### Example:
    ```python
    from app.logic.database import db

    credentials = {
        'host':     '127.0.0.1',
        'user':     'root',
        'password': 'root',
        'database': 'mysql_db',
        'port':      3306,
    }

    db1 = database.db(credentials=credentials)
    db2 = database.db(credentials=None)

    assert db1 is db2  # True, both variables point to the same instance.
    ```

    #### Compatible DBMS:

    - MySQL
    - MariaDB
    """

    credentials = None

    def __init__(self, credentials: dict=None) -> None:
        """
        Initialize the database class.
        If credentials are not provided, it will use the existing instance.
        Args:
            credentials (dict): A dictionary containing the database connection details.
        Example:
            ```python
            from app.logic.database import db

            credentials = {
                'host':     '127.0.0.1',
                'user':     'root',
                'password': 'root',
                'database': 'mysql_db',
                'port':      3306,
            }

            db = database.db(credentials=credentials)
            ```
        """
        self._conn = None
        self._cursor = None
        self._logger = logging.getLogger(__name__)
        if credentials is not None:
            db.credentials = credentials 
            self._connect(credentials)
        else:
            self._connect(db.credentials)

        self.delete_inactive_rentals()



    def _connect(self: object, credentials) -> None:
        """
        Connect to the database using the provided credentials.
        If credentials are not provided, it will use the existing connection.

        Args:
            credentials (dict): A dictionary containing the database connection details.
                - host (str): The hostname of the database server.
                - user (str): The username to connect to the database.
                - password (str): The password for the user.
                - database (str): The name of the database to connect to.
                - port (int): The port number for the database connection.
        
        ## Errors
            Raises an exception if the connection fails.
        """
        try:
            self._conn = mysql.connector.connect(**credentials)
            self._conn.autocommit = True
            self._cursor = self._conn.cursor()
            self._logger.info("Connected to the database")
        except mysql.connector.Error as e:
            self._logger.error(f"Error connecting to the database: {e}")
            raise



    def close(self: object) -> None:
        """
        Close the database connection and cursor.
        This method should be called when the database operations are complete.
        """
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()


    def is_connection_alive(self):
        try:
            self._conn.ping(reconnect=True)
            return True
        except mysql.connector.Error as e:
            return False


    def ensure_connection(self):
        if self._conn is None or self._cursor is None or not self.is_connection_alive():
            self._connect(self.credentials)



    def get_user(self: object, user_id: int) -> tuple[int, str, float]:
        """
        Get single user instance from the database by user ID.
        Args:
            user_id (int): The ID of the user to retrieve. (Primary key in the database)
        Returns:
            tuple: A tuple containing user information.
        
        Example:
            ```python
            db.get_user(1) -> (1, "Kari Normann", 125.0)
            ```
        """
        query = "SELECT * FROM users WHERE id = %s"
        self._cursor.execute(query, (user_id,))
        return self._cursor.fetchone()
    


    def get_scooter(self: object, scooter_id: int) -> tuple[int, float, float, int]:
        """
        Get single scooter instance from the database by scooter ID.
        Args:
            scooter_id (int): The ID of the scooter to retrieve. (Primary key in the database)
        Returns:
            tuple: A tuple containing scooter information.
        Example:
            ```python
            db.get_scooter(1) -> (1, 63.41947, 10.40174, 0)
            ```
        """
        query = "SELECT * FROM scooters WHERE uuid = %s"
        self._cursor.execute(query, (scooter_id,))
        return self._cursor.fetchone()
    


    def get_rental_by_id(self: object, rental_id: int) -> tuple[int, int, str, bool, str, str, float]:
        """
        Get single rental instance from the database by rental ID.
        Args:
            rental_id (int): The ID of the rental to retrieve. (Primary key in the database)
        Returns:
            tuple: A tuple containing rental information.
        Example:
            ```python
            db.get_rental_by_id(1) -> (1, 2, 3, False, "2023-10-01 12:00:00", "2023-10-01 12:30:00", 15.0)
            ```
        """
        query = "SELECT * FROM rentals WHERE id = %s"
        self._cursor.execute(query, (rental_id,))
        return self._cursor.fetchone()
    


    def get_active_rental_by_user(self: object, user_id: int) -> tuple[int, int, str, bool, str, str, float]:
        """
        Get active rental instance from the database by user ID.
        Args:
            user_id (int): The ID of the user to retrieve. (Primary key in the database)
        Returns:
            tuple: A tuple containing rental information.
        Example:
            ```python
            db.get_active_rental_by_user(1) -> (5, 1, 3, True, "2023-10-01 12:00:00", None, 0.0)
            ```
        """
        query = "SELECT * FROM rentals WHERE user_id = %s AND is_active = 1"
        self._cursor.execute(query, (user_id,))
        return self._cursor.fetchone()
    


    def get_active_rental_by_scooter(self: object, scooter_id: int) -> tuple[int, int, str, bool, str, str, float]:
        """
        Get active rental instance from the database by scooter ID.
        Args:
            scooter_id (int): The ID of the scooter to retrieve. (Primary key in the database)
        Returns:
            tuple: A tuple containing rental information.
        Example:
            ```python
            db.get_active_rental_by_scooter(1) -> (5, 1, 3, True, "2023-10-01 12:00:00", None, 0.0)
            ```
        """
        query = "SELECT * FROM rentals WHERE scooter_id = %s AND is_active = 1"
        self._cursor.execute(query, (scooter_id,))
        return self._cursor.fetchone()
    
    

    def rental_started(self:object, user_id: int, scooter_id: int) -> bool:
        """
        Start a rental for a user and scooter. Creates a new instance in db.rentals.
        Args:
            user_id (int): The ID of the user starting the rental.
            scooter_id (str): The ID of the scooter being rented.
        Returns:
            bool: True if the rental was successfully started, False otherwise.
        Example:
            ```python
            db.rental_started(5, 6) -> True
            ```
        """
        query = "INSERT INTO rentals (user_id, scooter_id, is_active, start_time, end_time, total_price) VALUES (%s, %s, 1, UTC_TIMESTAMP(), NULL, 0.0)"
        try:
            self._cursor.execute(query, (user_id, scooter_id))
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error starting rental: {e}")
            return False
        


    def rental_completed(self:object, user_id: int, price: float, lat: float, lon: float, status: int) -> bool:
        """
        Complete a rental for a user and scooter. Updates the rental instance in db.rentals and the
        scooter instance in db.scooters, marking its current location and status code.
        Args:
            user_id (int): The ID of the user completing the rental.
            price (float): The total price of the rental.
            location (dict): The new location of the scooter.
            status (int): The status of the scooter.
        Returns:
            bool: True if the rental was successfully completed, False otherwise.
        Example:
            ```python
            db.rental_completed(5, 15.0, {"latitude": 63.41947, "longitude": 10.40174}, 0) -> True
            ```
        """
        rental = self.get_active_rental_by_user(user_id)
        if rental is None:
            self._logger.error("Rental not found")
            return False
        rental_id = rental[0]
        scooter_id = rental[2]
        query = "UPDATE rentals SET is_active = 0, end_time = NOW(), total_price = %s WHERE user_id = %s AND scooter_id = %s AND id = %s"
        self._logger.debug(f"Params: {price}, {user_id}, {scooter_id}, {rental_id}, {lat}, {lon}, {status}")
        try:
            self._cursor.execute(query, (price, user_id, scooter_id, rental_id))
            self._conn.commit()
            self._logger.info(f"Rental completed: {rental_id}")
        except mysql.connector.Error as e:
            self._logger.error(f"Error completing rental: {e}")
            return False
        try:
            return self._update_scooter_info(scooter_id, lat, lon, status)
        except mysql.connector.Error as e:
            self._logger.error(f"Error updating scooter info: {e}")
        


    def update_scooter_status(self: object, scooter_id: int, status: int) -> bool:
        query = "UPDATE scooters SET status = %s WHERE uuid = %s"
        self._logger.info(f"update_scooter_status: params: {status}, {scooter_id}")
        try:
            self._cursor.execute(query, (status, scooter_id))
            self._conn.commit()
            self._logger.info(f"Scooter info updated: {scooter_id}")
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error updating scooter info: {e}")
            return False



    def _update_scooter_info(self: object, scooter_id: int, lat: float, lon: float, status: int) -> bool:
        """
        Internal function to update the scooter information in the database.
        Args:
            scooter_id (str): The ID of the scooter to update.
            location (dict): The new location of the scooter.
            status (int): The status of the scooter.
        Returns:
            bool: True if the scooter information was successfully updated, False otherwise.
        """
        query = "UPDATE scooters SET latitude = %s, longtitude = %s, status = %s WHERE uuid = %s"
        self._logger.info(f"_update_scooter_info: params: {lat}, {lon}, {status}, {scooter_id}")
        try:
            self._cursor.execute(query, (lat, lon, status, scooter_id))
            self._conn.commit()
            self._logger.info(f"Scooter info updated: {scooter_id}")
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error updating scooter info: {e}")
            return False
        


    def get_all_scooters(self: object) -> list[tuple[int, float, float, int]]:
        """
        Get all scooters from the database.
        Returns:
            list: A list of dictionaries containing scooter information.
        """
        query = "SELECT * FROM scooters"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    


    def get_all_users(self: object) -> list[tuple[int, str, float]]:
        """
        Get all users from the database.
        Returns:
            list: A list of dictionaries containing user information.
        """
        query = "SELECT * FROM users"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    


    def get_all_rentals(self: object) -> list[tuple[int, int, str, bool, str, str, float]]:
        """
        Get all rentals from the database.
        Returns:
            list: A list of dictionaries containing rental information.
        """
        query = "SELECT * FROM rentals"
        self._cursor.execute(query)
        return self._cursor.fetchall()
    


    def get_active_rentals(self: object) -> list[tuple[int, int, str, bool, str, str, float]]:
        """
        Get all active rentals from the database.
        Returns:
            list: A list of dictionaries containing active rental information.
        """
        query = "SELECT * FROM rentals WHERE is_active = 1"
        self._cursor.execute(query)
        return self._cursor.fetchall()



    def delete_inactive_rentals(self: object) -> bool:
        """
        Delete all inactive rentals from the database.
        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query = "DELETE FROM rentals WHERE is_active = 0"
        try:
            self._cursor.execute(query)
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error deleting inactive rentals: {e}")
            return False
        


    def get_scooter_near_location(self: object, location: dict) -> list[tuple[str, float, float, int]]:
        """
        Get all scooters near a given location.
        Args:
            location (dict): A dictionary containing the latitude+-0.1 and longitude+-0.1 of the location.
        Returns:
            tuple: A list containing tuples containing scooter information.
        Example:
            ```python
            db.get_scooter_near_location({"latitude": 63.41947, "longitude": 10.40174}) -> 
            [(1, 63.40947, 10.41174, 0), (2, 63.42947, 10.39174, 0)]
            ```
        """
        query = "SELECT * FROM scooters WHERE latitude BETWEEN %s AND %s AND longtiude BETWEEN %s AND %s"
        latitude = location["latitude"]
        longitude = location["longitude"]
        self._cursor.execute(query, (latitude - 0.01, latitude + 0.01, longitude - 0.01, longitude + 0.01))
        return self._cursor.fetchall()
    


    def add_user(self: object, name: str, funds: float) -> bool:
        """
        Add a new user to the database.
        Args:
            name (str): The name of the user.
            funds (float): The initial funds for the user.
        Returns:
            bool: True if the user was successfully added, False otherwise.
        Example:
            ```python
            db.add_user("John Doe", 350.0) -> True
            ```
        """
        if funds < 0:
            self._logger.error("Funds cannot be negative")
            return False
        query = "INSERT INTO users (name, funds) VALUES (%s, %s)"
        try:
            self._cursor.execute(query, (name, funds))
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error adding user: {e}")
            return False
        


    def add_scooter(self: object, latitude: float, longitude: float, status: int) -> bool:
        """
        Add a new scooter to the database.
        Args:
            latitude (float): The latitude of the scooter.
            longitude (float): The longitude of the scooter.
            status (int): The status of the scooter.
        Returns:
            bool: True if the scooter was successfully added, False otherwise.
        Example:
            ```python
            db.add_scooter(63.41947, 10.40174, 0) -> True
            ```
        """
        query = "INSERT INTO scooters (latitude, longtitude, status) VALUES (%s, %s, %s)"
        try:
            self._cursor.execute(query, (latitude, longitude, status))
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error adding scooter: {e}")
            return False
        


    def charge_user(self: object, user_id: int, amount: float) -> bool:
        """
        Charge a user by reducing funds to their account.
        Args:
            user_id (int): The ID of the user to charge.
            amount (float): The amount to charge the user.
        Returns:
            bool: True if the user was successfully charged, False otherwise.
        Example:
            ```python
            db.get_user(1) -> (1, "Kari Normann", 125.0)
            db.charge_user(1, 50.0) -> True
            db.get_user(1) -> (1, "Kari Normann", 75.0)
            db.charge_user(1, -50.0) -> False
            db.get_user(1) -> (1, "Kari Normann", 75.0)
            ```
        """
        if amount <= 0:
            self._logger.error("Charge amount cannot be negative")
            return False
        query = "UPDATE users SET funds = funds - %s WHERE id = %s"
        try:
            self._cursor.execute(query, (amount, user_id))
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error charging user: {e}")
            return False
        


    def user_deposit(self: object, user_id: int, amount: float) -> bool:
        """
        Deposit funds to a user's account.
        Args:
            user_id (int): The ID of the user to deposit funds to.
            amount (float): The amount to deposit.
        Returns:
            bool: True if the deposit was successful, False otherwise.
        Example:
            ```python
            db.get_user(1) -> (1, "Kari Normann", 125.0)
            db.user_deposit(1, 50.0) -> True
            db.get_user(1) -> (1, "Kari Normann", 175.0)
            db.user_deposit(1, -50.0) -> False
            db.get_user(1) -> (1, "Kari Normann", 175.0)
            ```
        """
        if amount <= 0:
            self._logger.error("Deposit amount cannot be negative")
            return False
        query = "UPDATE users SET funds = funds + %s WHERE id = %s"
        try:
            self._cursor.execute(query, (amount, user_id))
            self._conn.commit()
            return True
        except mysql.connector.Error as e:
            self._logger.error(f"Error depositing to user: {e}")
            return False
        

    def user_has_active_rental(self: object, user_id: int) -> bool:
        """
        Check if a user has an active rental.
        Args:
            user_id (int): The ID of the user to check.
        Returns:
            bool: True if the user has an active rental, False otherwise.
        Example:
            ```python
            db.user_has_active_rental(1) -> True
            ```
        """
        query = "SELECT COUNT(*) FROM rentals WHERE user_id = %s AND is_active = 1"
        self._cursor.execute(query, (user_id,))
        return self._cursor.fetchone()[0] > 0
    

    def scooter_has_active_rental(self: object, scooter_id: int) -> bool:
        """
        Check if a scooter has an active rental.
        Args:
            scooter_id (int): The ID of the scooter to check.
        Returns:
            bool: True if the scooter has an active rental, False otherwise.
        Example:
            ```python
            db.scooter_has_active_rental(1) -> True
            ```
        """
        query = "SELECT COUNT(*) FROM rentals WHERE scooter_id = %s AND is_active = 1"
        self._cursor.execute(query, (scooter_id,))
        return self._cursor.fetchone()[0] > 0
