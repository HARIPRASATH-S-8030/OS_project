from PyQt6.QtWidgets import (
    QWidget,
    QTextEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from PyQt6.QtCore import QTimer

from states import State


class Viewer(QWidget):

    def __init__(self, engine):

        super().__init__()

        self.engine = engine


        self.setWindowTitle(
            "Secure Document Viewer"
        )

        self.setFixedSize(
            600,
            400
        )


        # Main Layout
        layout = QVBoxLayout()


        # Document display area
        self.document = QTextEdit()

        self.document.setText(
            "CONFIDENTIAL DOCUMENT\n\n"
            "This content exists only during "
            "the secure rendering session."
        )


        # Status display
        self.status = QLabel(
            "Views Remaining: 5"
        )


        # Next view button
        self.button = QPushButton(
            "Read Next View"
        )


        self.button.clicked.connect(
            self.read_file
        )


        # Add widgets
        layout.addWidget(
            self.document
        )

        layout.addWidget(
            self.status
        )

        layout.addWidget(
            self.button
        )


        self.setLayout(layout)


        # Start monitoring Policy Engine
        self.timer = QTimer()

        self.timer.timeout.connect(
            self.check_state
        )

        self.timer.start(1000)



    def read_file(self):

        try:

            # Inform Policy Engine about file access
            self.engine.view_file()


            # Update remaining views if available
            if hasattr(
                self.engine,
                "views_remaining"
            ):

                self.status.setText(
                    f"Views Remaining: "
                    f"{self.engine.views_remaining}"
                )


        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )



    def check_state(self):

        current_state = self.engine.state


        print(
            "Current State:",
            current_state
        )


        if current_state == State.SANITIZING:


            # Clear displayed sensitive data
            self.document.clear()


            # Stop timer
            self.timer.stop()


            QMessageBox.warning(
                self,
                "Security Alert",
                "Session expired or policy violated.\n"
                "Secure memory wiped."
            )


            # Close viewer
            self.close()