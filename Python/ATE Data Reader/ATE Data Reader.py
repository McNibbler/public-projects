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

# The purpose of this program is to attempt to make sense of Teradyne's somewhat-standard fie format: the
# Standard Test Data Format (STDF). This proprietary file format consists of non-trivially parsed and encoded
# binary data and is the most commonly used format of data produced by Automatic Test Equipment (ATE), used by
# companies like LTX-Credence and Teradyne. This program will be using the obscure but very helpful PySTDF library
# to parse and subsequently process the data into sensible, meaningful results.

# This project can be found here: https://github.com/McNibbler/public-projects/tree/master/Python/ATE%20Data%20Reader
#   Note: repository contains more projects than just ATE Reader

# The PySTDF library project can be found here: https://github.com/cmars/pystdf

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
    data = open(parsedDataFile).readlines()

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

    # Just to check that it worked. I'll get rid of this later
    print(far_data[0:5])
    print(len(far_data))
    print(mir_data[0:5])
    print(len(mir_data))
    print(sdr_data[0:5])
    print(len(sdr_data))
    print(pmr_data[0:5])
    print(len(pmr_data))
    print(pgr_data[0:5])
    print(len(pgr_data))
    print(pir_data[0:5])
    print(len(pir_data))
    print(ptr_data[0:5])
    print(len(ptr_data))
    print(prr_data[0:5])
    print(len(prr_data))
    print(tsr_data[0:5])
    print(len(tsr_data))
    print(hbr_data[0:5])
    print(len(hbr_data))
    print(sbr_data[0:5])
    print(len(sbr_data))
    print(pcr_data[0:5])
    print(len(pcr_data))
    print(mrr_data[0:5])
    print(len(mrr_data))

    # finds the number of lines per test, one line for each site being tested
    sdr_parse = sdr_data[0].split("|")
    number_of_sites = sdr_parse[3]
    print(number_of_sites)

    # This is legit gonna be like an array of data frames yikes
    ptr_data_frames = []

    for i in range (0, (len(ptr_data) / number_of_sites) - 1):
        test_number = ptr_data[i].split("|")[1]

        # I'll figure this one out soon enough omg this is so fugly
        # ptr_data_frames.append(pd.DataFrame(str(test_number):[]))


    # ignore this for now

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