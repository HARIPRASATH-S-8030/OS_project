"""
View Manager

Responsible for:
1. Tracking remaining views
2. Determining when the view limit is reached
"""

from config import DEFAULT_VIEW_LIMIT
from logger import PolicyLogger


class ViewManager:

    def __init__(self, max_views=DEFAULT_VIEW_LIMIT):
        self.max_views = max_views
        self.remaining_views = max_views

    def consume_view(self):
        """
        Consume one view.
        """

        if self.remaining_views > 0:
            self.remaining_views -= 1

            PolicyLogger.info(
                f"View Consumed. Remaining = {self.remaining_views}"
            )

    def limit_reached(self):
        """
        Returns True if no views remain.
        """

        return self.remaining_views == 0

    def reset(self):
        self.remaining_views = self.max_views

        PolicyLogger.info("View Counter Reset")

if __name__ == "__main__":

    view = ViewManager()

    print(view.limit_reached())

    view.consume_view()

    print(view.limit_reached())

    view.reset()