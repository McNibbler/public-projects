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

        # Have to read the imported .txt file but I'm not totally sure how
        self.data = None
        self.far_data, self.mir_data, self.sdr_data, self.pmr_data, self.pgr_data, self.pir_data, self.ptr_data, self.prr_data, self.tsr_data, self.hbr_data, self.sbr_data, self.pcr_data, self.mrr_data = [], [], [], [], [], [], [], [], [], [], [], [], []

        self.number_of_sites = None
        self.list_of_test_numbers = [['', 'ALL DATA']]
        self.list_of_test_numbers_string = []

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
        self.txt_upload_button.clicked.connect(self.open_text)

        # Generates a summary of the loaded text
        self.generate_summary_button = QPushButton('Generate summary of all results')
        self.generate_summary_button.setToolTip('Generate a results .csv summary for the uploaded parsed .txt')

        # Selects a test result for the desired
        self.select_test_menu = QComboBox()
        self.select_test_menu.setToolTip('Select the tests to produce the PDF results for')

        # Button to generate the test results for the desired tests from the selected menu
        self.generate_pdf_button = QPushButton('Generate .pdf from selected tests')
        self.generate_pdf_button.setToolTip('Generate a .pdf file with the selected tests from the parsed .txt')

        self.WINDOW_SIZE = (600, 180)
        self.file_path = None
        self.text_file_location = self.file_path

        self.setFixedSize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
        self.center()
        self.setWindowTitle('ATE Data Reader')

        self.file_selected = False

        self.main_window()


    # Main interface method
    def main_window(self):

        # Layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Adds the widgets together in the grid
        layout.addWidget(self.status_text, 0, 0, 1, 2)
        layout.addWidget(self.stdf_upload_button, 1, 0)
        layout.addWidget(self.stdf_upload_button_xlsx, 1, 1)
        layout.addWidget(self.txt_upload_button, 2, 0, 1, 2)
        layout.addWidget(self.generate_summary_button, 3, 0, 1, 2)
        layout.addWidget(self.select_test_menu, 4, 0)
        layout.addWidget(self.generate_pdf_button, 4, 1)

        # Window settings
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
        filterboi = 'STDF (*.stdf *.std)'
        filepath = QFileDialog.getOpenFileName(caption='Open STDF File', filter=filterboi)

        if filepath[0] == '':

            self.status_text.setText('Please select a file')
            pass

        else:

            self.status_text.update()
            FileReaders.process_file(filepath[0])
            self.status_text.setText(str(filepath[0].split('/')[-1] + '_parsed.txt created!'))


    # Opens and reads a file to parse the data to an xlsx
    def open_parsing_dialog_xlsx(self):

        self.status_text.setText('Parsing to .xlsx, please wait...')
        filterboi = 'STDF (*.stdf *.std)'
        filepath = QFileDialog.getOpenFileName(caption='Open STDF File', filter=filterboi)

        if filepath[0] == '':

            self.status_text.setText('Please select a file')
            pass

        else:

            self.status_text.update()
            FileReaders.to_excel(filepath[0])
            self.status_text.setText(str(filepath[0].split('/')[-1] + '_excel.xlsx created!'))


    # Opens and reads a file to parse the data
    def open_text(self):

        if self.file_selected:

            self.status_text.setText('Parsed .txt file already uploaded. Please restart program to upload another.')
            pass

        else:

            filterboi = 'Text (*.txt)'
            filepath = QFileDialog.getOpenFileName(caption='Open .txt File', filter=filterboi)

            self.file_path = filepath[0]

            if self.file_path is not '':

                self.data = open(self.file_path).read().splitlines()

                for i in range(0, len(self.data) - 1):
                    if self.data[i].startswith("FAR"):
                        self.far_data.append(self.data[i])
                    elif self.data[i].startswith("MIR"):
                        self.mir_data.append(self.data[i])
                    elif self.data[i].startswith("SDR"):
                        self.sdr_data.append(self.data[i])
                    elif self.data[i].startswith("PMR"):
                        self.pmr_data.append(self.data[i])
                    elif self.data[i].startswith("PGR"):
                        self.pgr_data.append(self.data[i])
                    elif self.data[i].startswith("PIR"):
                        self.pir_data.append(self.data[i])
                    elif self.data[i].startswith("PTR"):
                        self.ptr_data.append(self.data[i])
                    elif self.data[i].startswith("PRR"):
                        self.prr_data.append(self.data[i])
                    elif self.data[i].startswith("TSR"):
                        self.tsr_data.append(self.data[i])
                    elif self.data[i].startswith("HBR"):
                        self.hbr_data.append(self.data[i])
                    elif self.data[i].startswith("SBR"):
                        self.sbr_data.append(self.data[i])
                    elif self.data[i].startswith("PCR"):
                        self.pcr_data.append(self.data[i])
                    elif self.data[i].startswith("MRR"):
                        self.mrr_data.append(self.data[i])

                sdr_parse = self.sdr_data[0].split("|")
                self.number_of_sites = int(sdr_parse[3])


                self.list_of_test_numbers = [['', 'ALL DATA']]
                # Gathers a list of the test numbers and the tests ran for each site, avoiding repeats from rerun tests
                for i in range(0, len(self.ptr_data), self.number_of_sites):
                    if [self.ptr_data[i].split("|")[1], self.ptr_data[i].split("|")[7]] in self.list_of_test_numbers:
                        pass
                    else:
                        self.list_of_test_numbers.append([self.ptr_data[i].split("|")[1], self.ptr_data[i].split("|")[7]])

                self.list_of_test_numbers_string = []

                for i in range(0, len(self.list_of_test_numbers)):

                    self.list_of_test_numbers_string.append(str(self.list_of_test_numbers[i][1]))

                self.file_selected = True

                self.select_test_menu.addItems(self.list_of_test_numbers_string)

                self.status_text.setText('Parsed .txt uploaded!')

                self.main_window()

            else:

                self.status_text.setText('Please select a file')
                pass



    # Gets the list of tests from a parsed text file
    def get_list(self, string):
        if string is None or string == '':
            return ['ALL TESTS']


# Execute me
if __name__ == '__main__':
    app = QApplication(sys.argv)

    nice = Application()

    sys.exit(app.exec_())
