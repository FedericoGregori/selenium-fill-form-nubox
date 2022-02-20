"""
Timer suppo
"""
import time
from datetime import datetime


class Timer:
    """
    Timer class to measure time of execution.
    """

    def __init__(self, under_timing=None):
        self.__under_timing = under_timing
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.end = time.time()

    def elapsed(self):
        """
        Print elapsed time.
        """
        elapsed = datetime.fromtimestamp(self.end - self.start)
        return f"{self.__under_timing} took {elapsed.minute}m {elapsed.second}s"
