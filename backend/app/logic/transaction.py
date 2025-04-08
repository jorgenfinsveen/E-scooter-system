import os
from logic import database

DISABLE_TRANSACTIONS = os.getenv("DISABLE_TRANSACTIONS", "False").lower() == "true"
TRANSACTION_COST_UNLOCK = int(os.getenv('TRANSACTION_COST_UNLOCK', '10'))
TRANSACTION_COST_PER_MINUTE = int(os.getenv('TRANSACTION_COST_PER_MINUTE', '10'))
TRANSACTION_CORIDE_DISCOUNT_PER_EXTRA_PERSON = int(os.getenv('TRANSACTION_CORIDE_DISCOUNT_PER_EXTRA_PERSON', '10'))

db = None

def _init_db_client() -> None:
    """
    Set the database client for the transaction module.
    The database client is fetched as a singleton instance.
    """
    global db
    db = database.db()

def validate_funds(user: dict, price: float) -> tuple[bool, str]:
    """
    Validate that the user has sufficient funds to make a purchase.

    Args:
        user (dict): A dictionary containing representing the user.
        price (float): Estimated price of the renting-time.

    Returns:
        Tuple: 
         * [0]: _bool_. True if the user has sufficient funds, False otherwise.
         * [1]: _str_. A message indicating the result of the validation.
                 
        __Example__
    ```python
        validate_funds(user, 32.5) ->
        (True, "Funds validated") 

        validate_funds(user, 100.0) ->
        (False, "Insufficient funds")
    ```
    """
    if DISABLE_TRANSACTIONS:
        return True, "transactions disabled", ""
    if db is None:
        _init_db_client()
    try:
        if user['funds'] < price:
            return False, "insufficient funds", "insufficient-funds"
        return True, "funds validated", ""
    except Exception as e:
        return False, f"error validating funds: {e}", "insufficient-funds"




def _process_transaction(user: dict, price: float) -> tuple[bool, str, float]:
    """
    Process a transaction for a user. Deducts the price from the user's balance.

    Args:
        user (dict): Object representing the user.
        price (float): The price of the renting-time.
        
    Returns:
        Tuple: 
         * [0]: _bool_. True if the user has sufficient funds, False otherwise.
         * [1]: _str_. A message indicating the result of the transaction.
                          
        __Example__
    ```python
        process_transaction(user, 32.5) ->
        (True, "Transaction successful") 
    ```
    """
    if DISABLE_TRANSACTIONS:
        return True, "transactions disabled", -1.0
    if db is None:
        _init_db_client()
    try: 
        if user['funds'] < price:
            return False, "insufficient funds", price
        else:
            return True, "transaction successful", price
    except Exception as e:
        return False, f"error processing transaction: {e}"
    

def pay_for_single_ride(user: dict, minutes: float) -> tuple[bool, str, float]:
    """
    Process a transaction for a single ride. Deducts the price from the user's balance.
    Args:
        user (dict): Object representing the user.
        minutes (float): Time of the ride in minutes.
    """
    price = round(TRANSACTION_COST_UNLOCK + (minutes * TRANSACTION_COST_PER_MINUTE),1)
    return _process_transaction(user, price)


def pay_for_coride_ride(users: list, minutes: float, num_coriders: int) -> tuple[bool, str]:
    """
    Process a transaction for a coride ride. Deducts the price from the users' balance.
    Args:
        users (list): List of user objects.
        minutes (float): Time of the ride in minutes.
        num_coriders (int): Number of coriders.
    """
    for user in users:
        price = TRANSACTION_COST_UNLOCK + (minutes * TRANSACTION_COST_PER_MINUTE) - (num_coriders * TRANSACTION_CORIDE_DISCOUNT_PER_EXTRA_PERSON)
        if _process_transaction(user, price)[0] == False:
            return False, f"insufficient funds - user: {user['name']}"
    return True, "transaction successful"
