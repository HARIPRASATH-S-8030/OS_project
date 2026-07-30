from PyQt6.QtWidgets import (
    QWidget,
    QTextEdit,
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

        self.setWindowTitle("Secure Document Viewer")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()

        # Document Display
        self.document = QTextEdit()
        self.document.setReadOnly(True)

        self.document.setText(
            "CONFIDENTIAL DOCUMENT\n\n"
            "This content exists only during the secure rendering session."
        )

        # Close Secure Document Button
        self.close_button = QPushButton("Close Document")
        self.close_button.clicked.connect(self.end_session)

        layout.addWidget(self.document)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        # Timer to monitor policy state
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_state)
        self.timer.start(1000)

    def end_session(self):
        """
        Notify the Policy Engine that the user has finished viewing.
        The Policy Engine should transition to SANITIZING/TERMINATED.
        """

        try:
            self.engine.view_file()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def check_state(self):

        state = self.engine.state

        print("Current State:", state)

        if state in (
            State.SANITIZING,
            State.TERMINATED
        ):

            self.timer.stop()

            self.document.clear()

            QMessageBox.information(
                self,
                "Session Ended",
                "This document was available for one-time viewing only.\n\n"
                "The secure session has ended and memory has been wiped."
            )

            self.close()