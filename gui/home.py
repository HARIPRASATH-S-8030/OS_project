from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from states import State


class HomeScreen(QWidget):

    def __init__(self, engine):

        super().__init__()

        self.engine = engine

        self.login_window = None

        self.setWindowTitle(
            "Secure File Sharing"
        )

        self.setFixedSize(
            400,
            300
        )


        # Layout
        layout = QVBoxLayout()


        # Title
        title = QLabel(
            "Secure File Sharing"
        )


        # Open document button
        open_button = QPushButton(
            "Open Document"
        )


        open_button.clicked.connect(
            self.open_document
        )


        layout.addWidget(title)
        layout.addWidget(open_button)


        self.setLayout(layout)



    def open_document(self):

        try:

            # Send request to Policy Engine
            self.engine.open_file()


            # Check Policy Engine state
            if self.engine.state == State.AUTHENTICATING:

                print(
                    "Authentication required"
                )

                self.open_login()


            else:

                print(
                    "Current State:",
                    self.engine.state
                )


        except Exception as e:

            QMessageBox.critical(
                self,
                "Policy Engine Error",
                str(e)
            )



    def open_login(self):

        from login import LoginScreen


        self.login_window = LoginScreen(
            self.engine
        )


        self.login_window.show()


        self.close()