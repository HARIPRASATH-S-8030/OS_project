import sys

from PyQt6.QtWidgets import QApplication

from home import HomeScreen


class SecureFileApp:

    def __init__(self):

        self.window = HomeScreen()
        self.window.show()



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SecureFileApp()

    sys.exit(app.exec())