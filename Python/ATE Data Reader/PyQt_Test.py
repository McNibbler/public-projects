# Probably not doing anything meaningful here, but I want to test how pyqt works over tkinter
# Credits to ZetCode for the tutorial

###################################################

import sys
# from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QToolTip, QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os

from pystdf.IO import *
from pystdf.Writers import *

import pystdf.V4 as V4
from pystdf.Importer import STDF2DataFrame

import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
import pandas as pd

from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfFileMerger, PdfFileReader

###################################################


# We're living that object oriented life now
# Here's where I put my functions for reading files
class FileReaders:

    # processing that big boi
    @staticmethod
    def process_file(filename):
        # Lets you know what's goin' on
        print('Parsing data...')
        print()

        # Open that bad boi up
        f = open(filename, 'rb')
        reopen_fn = None

        # The name of the new file, preserving the directory of the previous
        newFile = filename + "_parsed.txt"

        # I guess I'm making a parsing object here, but again I didn't write this part
        p = Parser(inp=f, reopen_fn=reopen_fn)

        # Writing to a text file instead of vomiting it to the console
        with open(newFile, 'w') as fout:
            p.addSink(TextWriter(stream=fout))  # fout writes it to the opened text file
            p.parse()

        # We don't need to keep that file open
        f.close()

    # Parses that big boi but this time in Excel format (slow, don't use unless you wish to look at how it's organized)
    @staticmethod
    def to_excel(filename):
        # Converts the stdf to a data frame... somehow
        # (i do not ever intend on looking how he managed to parse this gross file format)
        tables = STDF2DataFrame(filename)

        # The name of the new file, preserving the directory of the previous
        fname = filename + "_excel.xlsx"

        # Writing object to work with excel documents
        writer = pd.ExcelWriter(fname, engine='xlsxwriter')

        # Not mine and I don't really know what's going on here, but it works, so I won't question him.
        # It actually write the data frame as an excel document
        for k, v in tables.items():
            # Make sure the order of columns complies the specs
            record = [r for r in V4.records if r.__class__.__name__.upper() == k]
            if len(record) == 0:
                print("Ignore exporting table %s: No such record type exists." % k)
            else:
                columns = [field[0] for field in record[0].fieldMap]
                v.to_excel(writer, sheet_name=k, columns=columns, index=False, na_rep="N/A")

        writer.save()


# Object oriented programming should be illegal cus i forgot how to be good at it
# These are the functions for the widget application objects that run the whole interface
class Application(QWidget):

    # Construct me
    def __init__(self):
        super().__init__()

        self.WINDOW_SIZE = (300, 200)
        self.main_window()

    # Main interface method
    def main_window(self):

        # # Default UI elements
        # WINDOW_SIZE = (300, 200)
        # # FONT = 'Raleway'
        # # FONT_SIZE = 12
        #
        #
        # layout = QGridLayout()
        # self.setLayout(layout)
        #
        # status_label = QLabel()
        # status_label.setText('Hello!')
        #
        # layout.addWidget(status_label, 0, 0)
        #
        # upload_button = QPushButton('Parse STD/STDF to .txt', self)
        # upload_button.setToolTip('Browse your files for a file ending in .std or .stdf to create a parsed .txt file to work with')
        # upload_button.resize(upload_button.sizeHint())
        # layout.addWidget(upload_button, 1, 0)
        #
        # upload_button.clicked.connect(self.open_parsing_dialog)
        #
        #
        # if not self.nice == '':
        #
        #     FileReaders.process_file(self.file_path)
        #     self.file_path = ''
        #
        #
        # self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        # self.center()
        # self.setWindowTitle('ATE Data Reader')
        # self.show()

        layout = QGridLayout()
        self.setLayout(layout)

        self.parsed_string = None

        self.status_text = QLabel()
        self.stdf_upload_button = QPushButton('Parse STD/STDF to .txt')
        self.txt_upload_button = QPushButton('Upload parsed .txt file')
        self.generate_summary_button = QPushButton('Generate summary of all results')

        self.select_test_menu = QComboBox()
        self.select_test_menu.addItems(self.get_list(self.parsed_string))

        self.generate_pdf_button = QPushButton('Generate .pdf from selected tests')



        layout.addWidget(self.status_text, 0, 0)
        layout.addWidget(self.stdf_upload_button, 1, 0)
        layout.addWidget(self.txt_upload_button, 2, 0)
        layout.addWidget(self.generate_summary_button, 3, 0)
        layout.addWidget(self.select_test_menu, 4, 0)
        layout.addWidget(self.generate_pdf_button, 5, 0)

        self.resize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
        self.center()
        self.setWindowTitle('ATE Data Reader')
        self.show()

    # Centers the window
    def center(self):
        window = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        window.moveCenter(center_point)
        self.move(window.topLeft())

    # Opens and reads a file to parse the data

    def open_parsing_dialog(self):
        filterboi = 'STDF (*.stdf, *.std)'
        filepath = QFileDialog.getOpenFileName(caption='Open STDF File', filter=filterboi)

        self.file_path = filepath[0]

    def get_list(self, string):

        if string == None or string == '':

            return ['ALL TESTS']

# Execute me
if __name__ == '__main__':
    app = QApplication(sys.argv)

    nice = Application()

    sys.exit(app.exec_())
