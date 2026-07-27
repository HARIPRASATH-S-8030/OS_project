from PyQt6.QtWidgets import *


class LoginScreen(QWidget):

    def __init__(self,engine):

        super().__init__()

        self.engine = engine


        layout = QVBoxLayout()


        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Enter Password"
        )


        button = QPushButton(
            "Submit"
        )


        button.clicked.connect(
            self.login
        )


        layout.addWidget(
            self.password
        )

        layout.addWidget(
            button
        )


        self.setLayout(layout)



    def login(self):

        password = self.password.text()


        self.engine.authenticate(
            password
        )


        print(
            self.engine.state
        )