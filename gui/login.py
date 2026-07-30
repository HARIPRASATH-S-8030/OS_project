import os
from PyQt6.QtWidgets import *
from states import State
from viewer import Viewer

class LoginScreen(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        
        self.setWindowTitle("Authentication")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password) # Masks the password with dots

        button = QPushButton("Submit")
        button.clicked.connect(self.login)

        layout.addWidget(self.password)
        layout.addWidget(button)

        self.setLayout(layout)

    def login(self):
        password = self.password.text()
        
        # Send password to the backend
        self.engine.authenticate(password)
        print("FSM State after login:", self.engine.state)

        # Check if the FSM granted access
        if self.engine.state == State.SECURE_RENDER:
            # 1. Create and show the Viewer window
            self.viewer_window = Viewer(self.engine)
            
            # 2. Try to load the top-secret payload from a text file
            payload_path = "secret_payload.txt"
            if os.path.exists(payload_path):
                with open(payload_path, "r") as file:
                    self.viewer_window.document.setText(file.read())
            else:
                self.viewer_window.document.setText(
                    "[TOP SECRET - IEEE DEMO]\n\n"
                    "Project SecureOS Launch Codes: 9948-ABX-772\n"
                    "If this text is found in a RAM dump after sanitization, the system has failed."
                )
                
            self.viewer_window.show()
            
            # 3. Close the login screen
            self.close()
        else:
            # Show error if authentication fails
            QMessageBox.warning(self, "Access Denied", "Authentication Failed or Account Locked!")