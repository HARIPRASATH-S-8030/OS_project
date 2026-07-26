from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)


class HomeScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Secure File Sharing"
        )

        self.setFixedSize(
            400,
            300
        )


        layout = QVBoxLayout()


        title = QLabel(
            "Secure File Sharing"
        )


        button = QPushButton(
            "Open Secure Document"
        )


        button.clicked.connect(
            self.open_document
        )


        layout.addWidget(title)
        layout.addWidget(button)


        self.setLayout(layout)



    def open_document(self):

        print("Open button clicked")