import os
from typing import Tuple

DISABLE_TRANSACTIONS = os.getenv("DISABLE_TRANSACTIONS", "False").lower() == "true"
TRANSACTION_COST_UNLOCK = int(os.getenv('DEPLOYMENT_MODE', '10'))
TRANSACTION_COST_PER_MINUTE = int(os.getenv('TRANSACTION_COST_PER_MINUTE', '10'))
TRANSACTION_CORIDE_DISCOUNT_PER_EXTRA_PERSON = int(os.getenv('TRANSACTION_CORIDE_DISCOUNT_PER_EXTRA_PERSON', '10'))



def validate_funds(funds: dict, price: float) -> Tuple[bool, str]:
    """
    Validate that the user has sufficient funds to make a purchase.

    Args:
        funds (dict): A dictionary containing the user's funds.
        price (float): Estimated price of the renting-time.

    Returns:
        Tuple: 
        [0] - bool. True if the user has sufficient funds, False otherwise.\\
        [1] - str. A message indicating the result of the validation.
    """
    if DISABLE_TRANSACTIONS:
        return True, "Transactions disabled"
    try:
        if funds['balance'] < price:
            return False, "Insufficient funds"
        return True, "Funds validated"
    except Exception as e:
        return False, f"Error validating funds: {e}"




def process_transaction(user: dict, price: float) -> Tuple[bool, str]:
    """
    Process a transaction for a user. Deducts the price from the user's balance.

    Args:
        user (dict): Object representing the user.
        price (float): The price of the renting-time.
        
    Returns:
        Tuple: 
        [0] - bool. True if the user has sufficient funds, False otherwise.\\
        [1] - str. A message indicating the result of the transaction.
    """
    if DISABLE_TRANSACTIONS:
        return True, "Transactions disabled"
    try: 
        if user['funds']['balance'] < price:
            return False, "Insufficient funds"
        else:
            user['funds']['balance'] -= price
            return True, "Transaction successful"
    except Exception as e:
        return False, f"Error processing transaction: {e}"
    

def pay_for_single_ride(user: dict, minutes: float) -> Tuple[bool, str]:
    price = TRANSACTION_COST_UNLOCK + (minutes * TRANSACTION_COST_PER_MINUTE)
    return process_transaction(user, price)


def pay_for_coride_ride(users: list, minutes: float, num_coriders: int) -> Tuple[bool, str]:
    for user in users:
        price = TRANSACTION_COST_UNLOCK + (minutes * TRANSACTION_COST_PER_MINUTE) - (num_coriders * TRANSACTION_CORIDE_DISCOUNT_PER_EXTRA_PERSON)
        if process_transaction(user, price)[0] == False:
            return False, f"Insufficient funds - user: {user['name']}"
    return True, "Transaction successful"
