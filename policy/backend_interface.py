"""
Backend Interface

Responsible for communication between the
Policy Engine (Python) and Backend (C++).
"""

from logger import PolicyLogger


class BackendInterface:

    def __init__(self):
        self.connected = False

    def connect(self):
        """
        Simulate establishing connection with backend.
        """

        self.connected = True

        PolicyLogger.info("Backend Connected")

    def disconnect(self):
        """
        Simulate backend disconnection.
        """

        self.connected = False

        PolicyLogger.info("Backend Disconnected")

    def send_sanitize_signal(self):
        """
        Send sanitize command to backend.
        """

        if not self.connected:

            PolicyLogger.warning(
                "Backend not connected. Cannot send sanitize signal."
            )

            return False

        PolicyLogger.info(
            "SANITIZE signal sent to backend."
        )

        return True

if __name__ == "__main__":

    backend = BackendInterface()

    backend.send_sanitize_signal()

    backend.connect()

    backend.send_sanitize_signal()

    backend.disconnect()