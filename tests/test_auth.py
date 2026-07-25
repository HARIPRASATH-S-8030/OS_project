"""
Unit Tests for Authentication Manager
"""

import sys
import os

# Add policy folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy")
    )
)

from auth_manager import AuthManager


def test_successful_login():
    print("\n========== TEST 1 : Successful Login ==========")

    auth = AuthManager(
        password="admin123",
        max_attempts=3
    )

    assert auth.authenticate("admin123") is True

    print("PASS")


def test_failed_login():
    print("\n========== TEST 2 : Failed Login ==========")

    auth = AuthManager(
        password="admin123",
        max_attempts=3
    )

    assert auth.authenticate("wrong") is False

    print("PASS")


def test_failure_limit():
    print("\n========== TEST 3 : Failure Limit ==========")

    auth = AuthManager(
        password="admin123",
        max_attempts=3
    )

    auth.authenticate("1")
    auth.authenticate("2")
    auth.authenticate("3")

    assert auth.limit_reached() is True

    print("PASS")


def test_reset():
    print("\n========== TEST 4 : Reset Counter ==========")

    auth = AuthManager(
        password="admin123",
        max_attempts=3
    )

    auth.authenticate("wrong")
    auth.authenticate("wrong")

    auth.reset()

    assert auth.failed_attempts == 0

    print("PASS")


if __name__ == "__main__":

    print("\nRunning Authentication Tests")

    test_successful_login()

    test_failed_login()

    test_failure_limit()

    test_reset()

    print("\nAll Authentication Tests Passed")