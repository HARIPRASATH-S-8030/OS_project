"""
Integration Test for Policy Engine
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

from policy_manager import PolicyEngine
from states import State


def test_complete_workflow():

    print("\n========== POLICY ENGINE INTEGRATION TEST ==========\n")

    engine = PolicyEngine(
        password="admin123",
        expiry_time=30,
        view_limit=2,
        max_failed_attempts=3
    )

    # Initial State
    assert engine.state == State.IDLE

    # Open File
    engine.open_file()
    assert engine.state == State.AUTHENTICATING

    # Authenticate
    engine.authenticate("admin123")
    assert engine.state == State.SECURE_RENDER

    # First View
    engine.view_file()
    assert engine.state == State.SECURE_RENDER

    # Second View (Triggers Sanitization)
    engine.view_file()

    # Give sanitization a moment to finish
    time.sleep(1)

    assert engine.state == State.TERMINATED

    print("\nPASS")
    print("\nPolicy Engine Workflow Verified Successfully")


if __name__ == "__main__":

    print("Running Policy Engine Integration Test")

    test_complete_workflow()

    print("\nIntegration Test Passed")