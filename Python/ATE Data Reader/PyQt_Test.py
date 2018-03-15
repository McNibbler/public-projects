# Probably not doing anything meaningful here, but I want to test how pyqt works over tkinter

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QIcon


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Rn im literally following a tutorial lmao"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()


if __name__ == 'main':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
