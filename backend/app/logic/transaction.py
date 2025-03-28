import os
from typing import Tuple

DISABLE_TRANSACTIONS = bool(os.getenv('DISABLE_TRANSACTIONS', True))



def validate_funds(funds: dict, price: int) -> Tuple[bool, str]:
    """
    Validate that the user has sufficient funds to make a purchase.

    Args:
        funds (dict): A dictionary containing the user's funds.
        price (int): Estimated price of the renting-time.

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




def process_transaction(user: dict, price: int) -> Tuple[bool, str]:
    """
    Process a transaction for a user. Deducts the price from the user's balance.

    Args:
        user (dict): Object representing the user.
        price (int): The price of the renting-time.
        
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