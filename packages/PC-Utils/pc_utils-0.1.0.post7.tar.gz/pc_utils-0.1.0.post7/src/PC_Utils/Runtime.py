"""
Created on:     7/1/2021
Created by:     Marcos E. Mercado
Description:    This module contains the Runtime class that encapsulates methods to calculate runtime
"""
import time

class Runtime:
    """This class uses time module and provides methods to show the current time in an easy to read format and friendly time units."""

    def __init__(self):
        self.creation_time_inSeconds = self.curr_time_inSeconds()

    def curr_time_inSeconds(self) -> float:
        return time.time()

    def friendly_time(self) -> str:
        return time.ctime()

    def strTimeStamp(self) -> str:
        return time.strftime("%Y%m%d_%H%M") # returns timestamp as for example: "20210708_1734"

    def get_runtime(self, start_time: float = None, end_time: float = None) -> str:
        """Method that compares the time elapsed between start and end and shows the difference in seconds or minutes.
        If none provided, it uses  current time vs. creation time."""
        if not start_time:  # if start_time was not provided, use creation time in seconds
            start_time = self.creation_time_inSeconds
   
        if not end_time:    # if end_time is not provided, use the current time in seconds
           end_time = self.curr_time_inSeconds()

        totalTime = end_time - start_time

        if totalTime < 120 :
            return str(totalTime) + " seconds"    # runtime in seconds
        else:
            return str(totalTime/60) + " minutes" # runtime in minutes

    def print_time(self, label: str = None) -> None:
        """Method to print the current time in a friendly format with the given string as a label."""
        if label is None:
            print(self.friendly_time())
        else:
            print(label, self.friendly_time(), sep="\t")

    def print_runtime(self, label: str = None) -> None:
        """Method to print the amount of time has passed since the class was instantiated with the given message as a label.
        Useful when timing how long the execution of a progam has taken up so far."""
        if label is None:
            print(self.get_runtime())
        else:
            print(label, self.get_runtime(), sep="\t")