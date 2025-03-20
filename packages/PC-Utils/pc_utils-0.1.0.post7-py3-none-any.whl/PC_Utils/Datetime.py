"""
Created on:     9/30/2024
Created by:     Marcos E. Mercado
Description:    Datetime class contains methods related to date/time manipulation.
"""
from datetime import datetime

class Datetime:
    """This class provides methods to manipulate or convert date/time values."""

    def __init__(self):
        self.current_time = datetime.now()

    def date_to_epoch(date_str: str, date_format: str ="%Y-%m-%d") -> int:
        """
        Converts a date string to an epoch timestamp.

        Args:
        - date_str (str): The date string to convert.
        - date_format (str): The format of the input date string. Default is "%Y-%m-%d".

        Returns:
        - int: The epoch timestamp corresponding to the input date.
        """
        # Convert the date string to a datetime object
        dt = datetime.strptime(date_str, date_format)
    
        # Convert the datetime object to an epoch timestamp
        epoch_time = int(dt.timestamp())
    
        return epoch_time
