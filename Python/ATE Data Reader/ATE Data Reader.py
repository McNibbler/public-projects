###################################################
# ATE STDF Data Reader Python Edition             #
# Version 0.2                                     #
#                                                 #
# March 2, 2018                                   #
# Thomas Kaunzinger                               #
# LTX-Credence / XCerra Corp.                     #
#                                                 #
# References:                                     #
# PySTDF Library                                  #
# numpy                                           #
# matplotlib                                      #
# My crying soul because there's no documentation #
###################################################

#######################################################################################################################
# The purpose of this program is to attempt to make sense of Teradyne's somewhat-standard fie format: the             #
# Standard Test Data Format (STDF). This proprietary file format consists of non-trivially parsed and encoded         #
# binary data and is the most commonly used format of data produced by Automatic Test Equipment (ATE), used by        #
# companies like LTX-Credence and Teradyne. This program will be using the obscure but very helpful PySTDF library    #
# to parse and subsequently process the data into sensible, meaningful results.                                       #
#                                                                                                                     #
# This project can be found here: https://github.com/McNibbler/public-projects/tree/master/Python/ATE%20Data%20Reader #
#   Note: repository contains more projects than just ATE Reader. Please check them out if you're interested :)       #
#                                                                                                                     #
# The PySTDF library project can be found here: https://github.com/cmars/pystdf                                       #
#######################################################################################################################

#######################################################################################################################
# NOTE: Do not run this program on data with the a file of the same name, but with "_parsed.txt" or "_excel.xlsx"     #
# appended to the end; e.g. running this on "data.std" with a file called "data.std_parsed.txt" in the same folder is #
# a bad idea, as it will be overwritten, due to the fact that this program creates and writes to a text file of that  #
# naming convention. But for real, why would you even do that in the first place?                                     #
#######################################################################################################################

###################################################

#######################
# IMPORTING LIBRARIES #
#######################

# Importing a bunch of stuff that I probably won't even need but we'll just roll with it for now. I actually don't even
# know what libraries here I actually am using at the moment so that's fun.
from __future__ import print_function

from pystdf.IO import *
from pystdf.Writers import *

import os
import sys

sys.path.append("/pystdf-master")

try:
    import gzip
    have_gzip = True
except ImportError:
    have_gzip = False

try:
    import bz2
    have_bz2 = True
except ImportError:
    have_bz2 = False

import pandas as pd
import pystdf.V4 as V4
from pystdf.Importer import STDF2DataFrame

gzPattern = re.compile('\.g?z', re.I)
bz2Pattern = re.compile('\.bz2', re.I)

import numpy as np
import matplotlib.pyplot as plt

###################################################

##################
# FILE SELECTION #
##################

# Chose where the STDF file is located. I'll add some pretty-ness to this at some point

wd = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(wd, "Data\\data.std")

print(filepath)


###################################################

###############
# MAIN METHOD #
###############

# Defining the main method
def main():
    # Parses that big boi into a text file
    # process_file(filepath)

    # This one is way too slow. Use with caution.
    # toExcel(filepath)

    # Finds and opens the recently created parsed text file
    parsedDataFile = filepath + "_parsed.txt"
    data = open(parsedDataFile).read().splitlines()

    # Checks that it's actually correct
    print(data[0:10])
    print(len(data))

    # Separates the different types of data from the text file into their own sets. Here, I am initializing the arrays.
    far_data = []
    mir_data = []
    sdr_data = []
    pmr_data = []
    pgr_data = []
    pir_data = []
    ptr_data = []
    prr_data = []
    tsr_data = []
    hbr_data = []
    sbr_data = []
    pcr_data = []
    mrr_data = []

    # Appends each set of data to their own personal arrays
    for i in range(0, len(data) - 1):
        if data[i].startswith("FAR"):
            far_data.append(data[i])
        elif data[i].startswith("MIR"):
            mir_data.append(data[i])
        elif data[i].startswith("SDR"):
            sdr_data.append(data[i])
        elif data[i].startswith("PMR"):
            pmr_data.append(data[i])
        elif data[i].startswith("PGR"):
            pgr_data.append(data[i])
        elif data[i].startswith("PIR"):
            pir_data.append(data[i])
        elif data[i].startswith("PTR"):
            ptr_data.append(data[i])
        elif data[i].startswith("PRR"):
            prr_data.append(data[i])
        elif data[i].startswith("TSR"):
            tsr_data.append(data[i])
        elif data[i].startswith("HBR"):
            hbr_data.append(data[i])
        elif data[i].startswith("SBR"):
            sbr_data.append(data[i])
        elif data[i].startswith("PCR"):
            pcr_data.append(data[i])
        elif data[i].startswith("MRR"):
            mrr_data.append(data[i])


    # finds the number of lines per test, one line for each site being tested
    sdr_parse = sdr_data[0].split("|")
    number_of_sites = int(sdr_parse[3])
    print(number_of_sites)


    # Finds the first testing number for the first set of data
    first_test = ptr_data[0].split("|")[1]


    # Gathers a list of the test numbers
    list_of_test_numbers = [first_test]
    for i in range(0, len(ptr_data), number_of_sites):
        list_of_test_numbers = np.vstack([list_of_test_numbers, ptr_data[i].split("|")[1]])


    # Extracts the PTR data from a given test number and stores it into an array
    selected_ptr_test = ptr_extractor(number_of_sites, ptr_data, first_test)

    # Test prints
    print(selected_ptr_test)
    print(len(selected_ptr_test))

    print(list_of_test_numbers)
    print(len(list_of_test_numbers))


    # all_ptr_tests = ptr_extractor(number_of_sites, ptr_data, first_test)




    ##########
    # IGNORE #
    ##########

    # # Lemme make sure I can get something to actually show up
    # plt.figure(1)
    #
    # # Raw Wave
    # plt.subplot(221)
    # plt.plot(tMili, data, color = "green")
    # plt.xlabel("Time (ms)")
    # plt.ylabel("Magnitude (V)")
    # plt.title("ADC Data (Raw)")
    #
    # plt.show()


###################################################

#######################
# IMPORTANT FUNCTIONS #
#######################

# Integer, Parsed List of Strings (PTR specifically), String -> Array
# It grabs the data for a certain test in the PTR data and turns that specific test into an array of arrays
def ptr_extractor(num_of_sites, data, test_number):

    # Initializes an array of the data from one of the tests for all test sites
    ptr_array_test = np.zeros(len(data[1].split("|")))

    # Finds where in the data to start looking for the test in question
    starting_index = 0
    for i in range(0, len(data), num_of_sites):
        if data[i].split("|")[1] == test_number:
            starting_index = i

    # Appends each row of the test's data to cover the entire test and nothing more
    for j in range (starting_index, (starting_index + num_of_sites)):
        ptr_array_test = np.vstack([ptr_array_test,data[j].split("|")])

    # Maybe I just suck at initializing arrays in numpy but I couldn't be bothered to do it without just creating an
    # array full of zeros first and then just removing it later.
    ptr_array_test = np.delete(ptr_array_test, 0, 0)

    # Returns the array weow!
    return ptr_array_test


# lmfao i just took this from the stdf2text script and im trying to change it so it works but there's no documentation
# im crying inside and out send help. I'll attempt to document it myself, but I'm so sorry for all the garbo.

# Currently, this function takes the stdf file and parses it to a text file with the name of the file, followed by a
# "_parsed.txt", which can be open and analyzed later. Parsing is delimited with pipes, "|"
def process_file(filename):
    # Not sure what this actually does but it was in the script so lets roll with it
    reopen_fn = None

    # Checks if gzip is installed and opens file with it if possible
    if gzPattern.search(filename):
        if not have_gzip:
            print("gzip is not supported on this system", file=sys.stderr)
            sys.exit(1)
        reopen_fn = lambda: gzip.open(filename, 'rb')
        f = reopen_fn()

    # Checks if bz2 is installed in the event that gzip isn't installed
    elif bz2Pattern.search(filename):
        if not have_bz2:
            print("bz2 is not supported on this system", file=sys.stderr)
            sys.exit(1)
        reopen_fn = lambda: bz2.BZ2File(filename, 'rb')
        f = reopen_fn()

    # Opens it the boring way otherwise (i don't actually know what makes this different, probably speed idk)
    else:
        f = open(filename, 'rb')

    # The name of the new file, preserving the directory of the previous
    newFile = filename + "_parsed.txt"

    # I guess I'm making a parsing object here, but again I didn't write this part
    p = Parser(inp=f, reopen_fn=reopen_fn)

    # Writing to a text file instead of vomiting it to the console
    with open(newFile, 'w') as fout:
        p.addSink(TextWriter(stream=fout))
        p.parse()

    # We don't need to keep that file open
    f.close()


# Similar to the previous function, takes an STDF file and creates an xlsx document with "_excel.xlsx" added to the file
# name. This function is hella slow, so I recommend not using it if you don't need to, but we'll see if I actually end
# up using it in this script or not.
def toExcel(filename):
    # Converts the stdf to a data frame... somehow (i do not ever intend on looking how he managed to parse this gross
    # file format)
    tables = STDF2DataFrame(filename)

    # The name of the new file, preserving the directory of the previous
    fname = filename + "_excel.xlsx"

    # Writing object to work with excel documents
    writer = pd.ExcelWriter(fname, engine='xlsxwriter')

    # Not mine and I don't really know what's going on here, but it works, so I won't question him. It actually writes
    # the data frame as an excel document
    for k, v in tables.items():
        # Make sure the order of columns complies the specs
        record = [r for r in V4.records if r.__class__.__name__.upper() == k]
        if len(record) == 0:
            print("Ignore exporting table %s: No such record type exists." % k)
        else:
            columns = [field[0] for field in record[0].fieldMap]
            v.to_excel(writer, sheet_name=k, columns=columns, index=False, na_rep="N/A")
    writer.save()


###################################################

#############
# EXECUTION #
#############

# Execute main method. Weow!!!
# If you made it this far, sorry for my passive-aggressive commenting and thanks for sticking through it all.
if __name__ == "__main__":
    main()