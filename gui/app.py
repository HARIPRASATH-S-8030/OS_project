import sys
import os


# Add policy directory to Python path
policy_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../policy"
    )
)


sys.path.insert(0, policy_path)
from PyQt6.QtWidgets import QApplication

from home import HomeScreen

# Import Dev B Policy Engine
from policy_manager import PolicyEngine
from states import State


# Create a global Policy Engine instance
engine = PolicyEngine()


class SecureFileApp:

    def __init__(self):

        # Pass PolicyEngine instance to GUI
        self.window = HomeScreen(engine)

        self.window.show()



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SecureFileApp()

    sys.exit(app.exec())