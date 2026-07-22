"""
Timer Manager

Responsible for:
1. Starting the expiry timer
2. Stopping the timer
3. Triggering a callback when time expires
"""

import threading

from config import DEFAULT_EXPIRY_TIME
from logger import PolicyLogger


class TimerManager:

    def __init__(self):
        self.timer = None
        self.running = False

    def start(self, callback, duration=DEFAULT_EXPIRY_TIME):
        """
        Start the expiry timer.
        callback -> Function to execute when timer expires.
        """

        self.stop()

        self.running = True

        PolicyLogger.info(f"Timer Started ({duration} seconds)")

        self.timer = threading.Timer(duration, callback)
        self.timer.start()

    def stop(self):
        """
        Stop the timer if running.
        """

        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
            self.running = False
            PolicyLogger.info("Timer Stopped")

    def is_running(self):
        """
        Returns True if timer is active.
        """

        return self.running

if __name__ == "__main__":

    def timer_expired():
        print(">>> TIMER CALLBACK EXECUTED <<<")

    timer = TimerManager()

    timer.start(timer_expired, duration=5)

    print("Waiting for timer...")

    input("Press ENTER after timer expires...")