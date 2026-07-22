from states import State
from events import Event

from auth_manager import AuthManager
from timer_manager import TimerManager
from view_manager import ViewManager

from logger import PolicyLogger


class PolicyEngine:

    def __init__(self):

        self.state = State.IDLE

        self.auth = AuthManager()

        self.timer = TimerManager()

        self.view = ViewManager()

        PolicyLogger.info("Policy Engine Initialized")

    def change_state(self, new_state):

        PolicyLogger.info(
            f"State Changed : {self.state.name} → {new_state.name}"
        )

        self.state = new_state

    def open_file(self):

        if self.state != State.IDLE:
            return

        self.change_state(State.AUTHENTICATING)

    def authenticate(self, password):

        if self.state != State.AUTHENTICATING:
            return

        if self.auth.authenticate(password):

            self.change_state(State.SECURE_RENDER)

            self.timer.start(self.timer_expired, duration=10)

        else:

            if self.auth.limit_reached():

                self.trigger_sanitization(
                 "Maximum Authentication Failures"
                )

    def view_file(self):
        """
        Called whenever the user opens/views the decrypted file.
        """

        if self.state != State.SECURE_RENDER:

            PolicyLogger.warning(
                "View request denied. File not in SECURE_RENDER state."
            )

            return

        self.view.consume_view()

        if self.view.limit_reached():

            PolicyLogger.warning("View Limit Reached")

            self.trigger_sanitization("View Count Exhausted")

    def sanitize(self):

        PolicyLogger.critical("Sanitization Triggered")

        self.timer.stop()

        self.auth.reset()

        self.view.reset()

        # Placeholder for Hari's backend
        PolicyLogger.info("Sending SANITIZE signal to backend")

        self.change_state(State.TERMINATED)

    def timer_expired(self):
        PolicyLogger.warning("Time Policy Violated")

        self.trigger_sanitization("Timer Expired")

    def trigger_sanitization(self, reason):
        """
        Centralized sanitization trigger.
        """

        PolicyLogger.critical(f"Policy Triggered: {reason}")

        if self.state != State.SANITIZING:
            self.change_state(State.SANITIZING)

        self.sanitize()

if __name__ == "__main__":

    engine = PolicyEngine()

    engine.open_file()

    engine.authenticate("admin123")

    print("\nViewing file...\n")

    engine.view_file()

    input("\nPress ENTER to exit...")