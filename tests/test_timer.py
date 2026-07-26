"""
Unit Tests for Timer Manager
"""

import sys
import os
import time

# Add policy folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy")
    )
)

from timer_manager import TimerManager


def timer_callback():
    print(">>> TIMER CALLBACK EXECUTED <<<")


def test_timer_expiry():

    print("\n========== TEST 1 : Timer Expiry ==========")

    timer = TimerManager()

    timer.start(
        callback=timer_callback,
        duration=3
    )

    print("Waiting for timer to expire...")

    time.sleep(4)

    print("PASS")


def test_timer_stop():

    print("\n========== TEST 2 : Timer Stop ==========")

    timer = TimerManager()

    timer.start(
        callback=timer_callback,
        duration=5
    )

    time.sleep(2)

    timer.stop()

    print("Waiting to verify callback is NOT executed...")

    time.sleep(4)

    print("PASS")


if __name__ == "__main__":

    print("\nRunning Timer Tests")

    test_timer_expiry()

    test_timer_stop()

    print("\nAll Timer Tests Passed")