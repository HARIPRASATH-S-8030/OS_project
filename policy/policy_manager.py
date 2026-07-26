from states import State
from events import Event

from auth_manager import AuthManager
from timer_manager import TimerManager
from view_manager import ViewManager
from backend_interface import BackendInterface  # <-- C++ Backend Bridge

from logger import PolicyLogger
from config import (
    DEFAULT_PASSWORD,
    DEFAULT_EXPIRY_TIME,
    DEFAULT_VIEW_LIMIT,
    MAX_FAILED_ATTEMPTS
)


class PolicyEngine:

    def __init__(
        self,
        password=DEFAULT_PASSWORD,
        expiry_time=DEFAULT_EXPIRY_TIME,
        view_limit=DEFAULT_VIEW_LIMIT,
        max_failed_attempts=MAX_FAILED_ATTEMPTS
    ):
        self.state = State.IDLE
        self.expiry_time = expiry_time
        
        # Managers initialized with config parameters
        self.auth = AuthManager(password=password, max_attempts=max_failed_attempts)
        self.timer = TimerManager()
        self.view = ViewManager(view_limit)
        
        # Real C++ Backend Interface integration
        self.backend = BackendInterface()
        
        PolicyLogger.info("Policy Engine Initialized")

    def change_state(self, new_state):
        PolicyLogger.info(
            f"State Changed : {self.state.name} → {new_state.name}"
        )
        self.state = new_state

    def open_file(self):
        if self.state != State.IDLE:
            return
        
        # Start the C++ backend process and lock memory when opening file
        if self.backend.connect():
            self.change_state(State.AUTHENTICATING)
        else:
            PolicyLogger.error("Failed to initialize secure backend storage.")

    def authenticate(self, password):
        if self.state != State.AUTHENTICATING:
            return

        if self.auth.authenticate(password):
            self.change_state(State.SECURE_RENDER)
            self.timer.start(self.timer_expired, duration=self.expiry_time)
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

        # Real integration: Dispatch hardware sanitization command to C++ backend
        PolicyLogger.info("Dispatching SANITIZE signal to C++ backend...")
        self.backend.send_sanitize_signal()

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
    # Initialize the engine
    engine = PolicyEngine()
    
    # 1. Open the file (Spawns C++ Backend and enters AUTHENTICATING)
    engine.open_file()
    
    # 2. Authenticate with default password from config
    engine.authenticate("admin123")
    
    print("\nViewing file...\n")
    
    # 3. Simulate viewing the file
    engine.view_file()
    
    input("\nPress ENTER to trigger sanitization and exit...")