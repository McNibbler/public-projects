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

from abc import ABC

import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
import pandas as pd

from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfFileMerger, PdfFileReader

###################################################


# We're living that object oriented life now
# Here's where I put my functions for reading files
class FileReaders(ABC):

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

        self.WINDOW_SIZE = (400, 180)
        self.file_path = None
        self.main_window()


    # Main interface method
    def main_window(self):

        # Layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Have to read the imported .txt file but I'm not totally sure how
        self.parsed_string = None

        # the status_text label lets you know the current status of the actions you are performing
        self.status_text = QLabel()
        self.status_text.setText('Welcome!')

        # Button to parse to .txt
        self.stdf_upload_button = QPushButton('Parse STD/STDF to .txt')
        self.stdf_upload_button.setToolTip('Browse for a file ending in .std or .stdf to create a parsed .txt file')
        self.stdf_upload_button.clicked.connect(self.open_parsing_dialog)

        # Button to parse to .xlsx
        self.stdf_upload_button_xlsx = QPushButton('Parse to .xlsx (not recommended)')
        self.stdf_upload_button_xlsx.setToolTip(
            'Browse for stdf to create .xlsx file. This is slow and unnecessary, but good for seeing parsed structure.')
        self.stdf_upload_button_xlsx.clicked.connect(self.open_parsing_dialog_xlsx)

        # Button to upload the .txt file to work with
        self.txt_upload_button = QPushButton('Upload parsed .txt file')
        self.txt_upload_button.setToolTip('Browse for the .txt file containing the parsed STDF data')

        # Generates a summary of the loaded text
        self.generate_summary_button = QPushButton('Generate summary of all results')
        self.generate_summary_button.setToolTip('Generate a results .csv summary for the uploaded parsed .txt')

        # Selects a test result for the desired
        self.select_test_menu = QComboBox()
        self.select_test_menu.setToolTip('Select the tests to produce the PDF results for')
        self.select_test_menu.addItems(self.get_list(self.parsed_string))

        # Button to generate the test results for the desired tests from the selected menu
        self.generate_pdf_button = QPushButton('Generate .pdf from selected tests')
        self.generate_pdf_button.setToolTip('Generate a .pdf file with the selected tests from the parsed .txt')


        # Adds the widgets together in the grid
        layout.addWidget(self.status_text, 0, 0, 1, 2)
        layout.addWidget(self.stdf_upload_button, 1, 0)
        layout.addWidget(self.stdf_upload_button_xlsx, 1, 1)
        layout.addWidget(self.txt_upload_button, 2, 0, 1, 2)
        layout.addWidget(self.generate_summary_button, 3, 0, 1, 2)
        layout.addWidget(self.select_test_menu, 4, 0)
        layout.addWidget(self.generate_pdf_button, 4, 1)

        # Window settings
        self.setFixedSize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
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
        self.status_text.setText('Parsing to .txt, please wait...')

        filterboi = 'STDF (*.stdf, *.std)'
        filepath = QFileDialog.getOpenFileName(caption='Open STDF File', filter=filterboi)

        FileReaders.process_file(filepath[0])
        self.status_text.setText(str(filepath[0].split('/')[-1] + '_parsed.txt created!'))


    # Opens and reads a file to parse the data to an xlsx
    def open_parsing_dialog_xlsx(self):
        self.status_text.setText('Parsing to .xlsx, please wait...')

        filterboi = 'STDF (*.stdf, *.std)'
        filepath = QFileDialog.getOpenFileName(caption='Open STDF File', filter=filterboi)

        FileReaders.to_excel(filepath[0])
        self.status_text.setText(str(filepath[0].split('/')[-1] + '_excel.xlsx created!'))


    # Gets the list of tests from a parsed text file
    def get_list(self, string):
        if string is None or string == '':
            return ['ALL TESTS']


# Execute me
if __name__ == '__main__':
    app = QApplication(sys.argv)

    nice = Application()

    sys.exit(app.exec_())
