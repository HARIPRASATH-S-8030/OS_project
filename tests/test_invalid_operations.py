"""
Edge Case Tests for Policy Engine
"""

import sys
import os

# Add policy folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy")
    )
)

from policy_manager import PolicyEngine
from states import State


def test_view_before_login():

    print("\n========== TEST 1 : View Before Login ==========")

    engine = PolicyEngine()

    engine.view_file()

    assert engine.state == State.IDLE

    print("PASS")


def test_auth_without_open():

    print("\n========== TEST 2 : Authenticate Without Opening ==========")

    engine = PolicyEngine()

    engine.authenticate("admin123")

    assert engine.state == State.IDLE

    print("PASS")


def test_open_twice():

    print("\n========== TEST 3 : Open File Twice ==========")

    engine = PolicyEngine()

    engine.open_file()

    engine.open_file()

    assert engine.state == State.AUTHENTICATING

    print("PASS")


def test_view_after_termination():

    print("\n========== TEST 4 : View After Termination ==========")

    engine = PolicyEngine(
        expiry_time=30,
        view_limit=1
    )

    engine.open_file()

    engine.authenticate("admin123")

    engine.view_file()

    engine.view_file()

    assert engine.state == State.TERMINATED

    print("Trying to view after termination...")

    engine.view_file()

    assert engine.state == State.TERMINATED

    print("PASS")


if __name__ == "__main__":

    print("Running Edge Case Tests")

    test_view_before_login()

    test_auth_without_open()

    test_open_twice()

    test_view_after_termination()

    print("\nAll Edge Case Tests Passed")