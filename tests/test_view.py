"""
Unit Tests for View Manager
"""

import sys
import os

# Add policy folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy")
    )
)

from view_manager import ViewManager


def test_single_view():

    print("\n========== TEST 1 : Single View ==========")

    view = ViewManager(max_views=2)

    view.consume_view()

    assert view.remaining_views == 1

    print("PASS")


def test_view_limit():

    print("\n========== TEST 2 : View Limit ==========")

    view = ViewManager(max_views=2)

    view.consume_view()
    view.consume_view()

    assert view.limit_reached() is True

    print("PASS")


def test_reset():

    print("\n========== TEST 3 : Reset Counter ==========")

    view = ViewManager(max_views=2)

    view.consume_view()
    view.consume_view()

    view.reset()

    assert view.remaining_views == 2

    print("PASS")


if __name__ == "__main__":

    print("\nRunning View Manager Tests")

    test_single_view()

    test_view_limit()

    test_reset()

    print("\nAll View Manager Tests Passed")