"""
Backend Interface

Responsible for communication between the
Policy Engine (Python) and Backend (C++).
"""

import subprocess
import os
import platform
from logger import PolicyLogger


class BackendInterface:

    def __init__(self, loader_path=None):
        if loader_path is None:
            # Automatically find build/loader from the project root
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Cross-platform executable extension handling (.exe for Windows)
            loader_filename = "loader.exe" if platform.system() == "Windows" else "loader"
            self.loader_path = os.path.join(base_dir, "build", loader_filename)
        else:
            self.loader_path = loader_path
            
        self.process = None
        self.connected = False

    def connect(self):
        """
        Spawns the real C++ backend process and locks memory.
        """
        if not os.path.exists(self.loader_path):
            PolicyLogger.error(f"Loader binary not found at {self.loader_path}. Compile it first!")
            return False

        try:
            # Change stdout=subprocess.PIPE to None so C++ prints directly to your terminal!
            self.process = subprocess.Popen(
                [self.loader_path],
                stdin=subprocess.PIPE,
                stdout=None,  # <-- This streams C++ output straight to your terminal screen
                stderr=None,  # <-- This streams C++ errors directly to your terminal screen
                text=True
            )
            self.connected = True
            PolicyLogger.info("Backend Connected (C++ Process Spawned)")
            return True
        except Exception as e:
            PolicyLogger.error(f"Failed to start C++ backend: {e}")
            return False

    def disconnect(self):
        """
        Terminate backend process if still running.
        """
        if self.process and self.process.poll() is None:
            self.process.terminate()
        self.connected = False
        PolicyLogger.info("Backend Disconnected")

    def send_sanitize_signal(self):
        """
        Send sanitize command to the C++ backend via stdin to wipe memory.
        """
        if not self.connected or not self.process:
            PolicyLogger.warning(
                "Backend not connected. Cannot send sanitize signal."
            )
            return False

        try:
            PolicyLogger.info("Sending SANITIZE signal to C++ backend...")
            self.process.stdin.write("SANITIZE\n")
            self.process.stdin.flush()
            
            # Wait briefly for process to handle zero-wiping and exit
            self.process.wait(timeout=2)
            PolicyLogger.info("SANITIZE signal acknowledged and executed by backend.")
            self.connected = False
            return True
        except Exception as e:
            PolicyLogger.error(f"Error communicating with backend during sanitization: {e}")
            if self.process:
                self.process.terminate()
            return False


if __name__ == "__main__":
    backend = BackendInterface()
    backend.connect()
    backend.send_sanitize_signal()