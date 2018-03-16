# Probably not doing anything meaningful here, but I want to test how pyqt works over tkinter
# Credits to ZetCode for the tutorial

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Application(QWidget):

    def __init__(self):
        super().__init__()

        self.main_window()

    def main_window(self):

        # Default UI elements
        WINDOW_LOCATION = (100, 100)
        WINDOW_SIZE = (300, 200)
        FONT = 'Raleway'
        FONT_SIZE = 12

        QToolTip.setFont(QFont(FONT, FONT_SIZE))

        upload_button = QPushButton('Upload STD/STDF', self)
        upload_button.setToolTip('Browse your files for a file ending in .std or .stdf')
        upload_button.resize(upload_button.sizeHint())
        upload_button.move(50, 50)

        self.setGeometry(WINDOW_LOCATION[0], WINDOW_LOCATION[1], WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.setWindowTitle('ATE Data Reader')
        self.show()

    def upload_event(self, event):



if __name__ == '__main__':
    app = QApplication(sys.argv)

    nice = Application()

    sys.exit(app.exec_())