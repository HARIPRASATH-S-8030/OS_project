from states import State
from events import Event


class PolicyEngine:

    def __init__(self):
        self.current_state = State.IDLE

        print(f"Policy Engine Initialized")
        print(f"Current State : {self.current_state}")

    def transition(self, event):
        """
        Handles all state transitions based on incoming events.
        """
        print(f"\nCurrent State : {self.current_state}")
        print(f"Received Event : {event}")

        if self.current_state == State.IDLE:

            if event == Event.OPEN_FILE:

                self.current_state = State.AUTHENTICATING

                print("Transition:")
                print("IDLE → AUTHENTICATING")
                print(f"New State : {self.current_state}")
        
        elif self.current_state == State.AUTHENTICATING:

            if event == Event.AUTH_SUCCESS:

                self.current_state = State.SECURE_RENDER

                print("Transition:")
                print("AUTHENTICATING → SECURE_RENDER")
                print(f"New State : {self.current_state}")

if __name__ == "__main__":
    engine = PolicyEngine()
    engine.transition(Event.OPEN_FILE)
    engine.transition(Event.AUTH_SUCCESS)