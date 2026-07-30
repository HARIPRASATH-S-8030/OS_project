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
                    "This file contains confidential information.\n" 
                    "If you are not the intended recepient, kindly erase this file.\n"
                )
                
            self.viewer_window.show()
            
            # 3. Close the login screen
            self.close()
        else:

            if self.engine.state == State.TERMINATED:

                QMessageBox.critical(
                    self,
                    "Access Blocked",
                    "Exceeded number of attempts.\n"
                    "You can no longer access this document."
                )

                self.close()

            else:

                QMessageBox.warning(
                    self,
                    "Access Denied",
                    "Authentication Failed!"
                )