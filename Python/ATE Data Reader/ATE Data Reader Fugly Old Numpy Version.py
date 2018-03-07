###################################################
# ATE STDF Data Reader Python Edition             #
# Version 0.4                                     #
#                                                 #
# March 7, 2018                                   #
# Thomas Kaunzinger                               #
# LTX-Credence / XCerra Corp.                     #
#                                                 #
# References:                                     #
# PySTDF Library                                  #
# numpy                                           #
# matplotlib                                      #
# My crying soul because there's no documentation #
###################################################

########################################################################################################################
# The purpose of this program is to attempt to make sense of Teradyne's somewhat-standard fie format: the              #
# Standard Test Data Format (STDF). This proprietary file format consists of non-trivially parsed and encoded          #
# binary data and is the most commonly used format of data produced by Automatic Test Equipment (ATE), used by         #
# companies like LTX-Credence and Teradyne. This program will be using the obscure but very helpful PySTDF library     #
# to parse and subsequently process the data into sensible, meaningful results.                                        #
#                                                                                                                      #
# This project can be found here: https://github.com/McNibbler/public-projects/tree/master/Python/ATE%20Data%20Reader  #
#   Note: repository contains more projects than just the ATE Reader. Please check them out if you're interested :)    #
#                                                                                                                      #
# The PySTDF library project can be found here: https://github.com/cmars/pystdf                                        #
########################################################################################################################

########################################################################################################################
# I also want to apologize in advance for some stupid code; e.g when I was creating arrays and I did something like:   #
#                                                                                                                      #
# np.zeros(...)                                                                                                        #
# SOME CODE TO DO SOMETHING TO THE ARRAY                                                                               #
# np.delete(... , 0, 0)                                                                                                #
#                                                                                                                      #
# I get this is really stupid, but frankly I haven't used python (or numpy at all) for anything like this in years and #
# I really can't be bothered to figure out the "proper" way to initialize and append to numpy arrays so this is my     #
# lazy solution and it works well enough for now so I don't really care if it looks stupid. Maybe I'll fix it later.   #
# It does not help that, going into this project, I had absolutely 0 experience with this file format and did not even #
# know what the end results were actually supposed to look like. Given that knowledge, please don't beat me up too     #
# badly for my messy and disorganized code. Thank you again and have mercy on me please :)                             #
########################################################################################################################

########################################################################################################################
# NOTE: Do not run this program on data with the a file of the same name, but with "_parsed.txt" or "_excel.xlsx"      #
# appended to the end; e.g. running this on "data.std" with a file called "data.std_parsed.txt" in the same folder is  #
# a bad idea, as it will be overwritten, due to the fact that this program creates and writes to a text file of that   #
# naming convention. But for real, why would you even do that in the first place?                                      #
########################################################################################################################

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
    far_data, mir_data, sdr_data, pmr_data, pgr_data, pir_data, ptr_data, prr_data, tsr_data, hbr_data, sbr_data, pcr_data, mrr_data = [], [], [], [], [], [], [], [], [], [], [], [], []

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

    # Selects a test number + name combination for a given index
    test_index = 200
    selected_test = [ptr_data[number_of_sites*test_index].split("|")[1], ptr_data[number_of_sites*test_index].split("|")[7]]

    # Finds the tuple of test number / test name for the first test in the file
    first_test = [ptr_data[0].split("|")[1], ptr_data[0].split("|")[7]]

    # Gathers a list of the test numbers and the tests ran for each site, avoiding repeats from rerun tests
    # Not used at the moment but who knows?
    list_of_test_numbers = []
    for i in range(0, len(ptr_data), number_of_sites):
        if (ptr_data[i].split("|")[1] in list_of_test_numbers) and (ptr_data[i].split("|")[7] in list_of_test_numbers):
            pass
        else:
            list_of_test_numbers.append([ptr_data[i].split("|")[1], ptr_data[i].split("|")[7]])


    print(selected_test)

    selected_test_all = find_tests_of_number(selected_test[0], list_of_test_numbers)
    print(selected_test_all)


    # Extracts the PTR data from a given test number + test name and stores it into an array
    selected_ptr_test = ptr_extractor(number_of_sites, ptr_data, selected_test)
    print(selected_ptr_test)
    print(selected_test)

    # # Extracts the PTR data for all test numbers selected in the list
    # all_ptr_test = []
    # for i in range(0, len(selected_test_all)):
    #     all_ptr_test.append(ptr_extractor(number_of_sites, ptr_data, selected_test_all[i]))
    # print(all_ptr_test)

    # Gathers each set of data from all runs for each site in one test, arranging them in a sequential array of arrays
    one_test = single_test_data(number_of_sites, selected_ptr_test)
    print(one_test)

    # # Gathers each set of data from all runs for each site in all selected tests
    # all_test = []
    # for i in range(len(all_ptr_test)):
    #     all_test.append(single_test_data(number_of_sites, all_ptr_test[i]))
    #
    # plot_list_of_tests(all_test, ptr_data, number_of_sites)


    # print(selected_test_all_data)


    # I'm so shook it's doing something I actually want it to do
    # Still needs a lot of love tho because this file is disorganized like all hell
    plt.figure()

    lower_limit = get_plot_min(ptr_data, selected_test, number_of_sites)
    upper_limit = get_plot_max(ptr_data, selected_test, number_of_sites)

    plot_full_test_trend(one_test, lower_limit, upper_limit)

    plt.xlabel("Test Number")
    plt.ylabel("Results")
    plt.title("Data Trendline")
    plt.grid(color='0.9', linestyle='--', linewidth=1)

    plt.show()



###################################################

#######################
# IMPORTANT FUNCTIONS #
#######################

def plot_list_of_tests(test_list, data, num_of_sites):
    for i in range(0, len(test_list)):
        plt.figure()
        low_lim = get_plot_min(data, test_list[i], num_of_sites)
        print(low_lim)
        hi_lim = get_plot_max(data, test_list[i], num_of_sites)
        print(hi_lim)
        print(test_list[i])
        plot_full_test_trend(test_list[i], low_lim, hi_lim)
        plt.show()



# TestNumber (string) + ListOfTests (list of tuples) -> ListOfTests with TestNumber as the 0th index (list of tuples)
# Takes a string representing a test number and returns any test names associated with that test number
#   e.g. one test number may be 1234 and might have 40 tests run on it, but it may be 20 tests under
#   the name "device_test_20kHz" and then another 20 tests under the name "device_test_100kHz", meaning
#   there were two unique tests run under the same test number.
def find_tests_of_number(test_number, test_list):
    tests_of_number = []
    for i in range(0, len(test_list)):
        if test_list[i][0] == test_number:
            tests_of_number.append(test_list[i])

    return tests_of_number


# Returns the lower allowed limit of a set of data
def get_plot_min(data, desired_test, num_of_sites):
    return get_plot_extremes(data, desired_test, num_of_sites)[0]

# Returns the upper allowed limit of a set of data
def get_plot_max(data, desired_test, num_of_sites):
    return get_plot_extremes(data, desired_test, num_of_sites)[1]

# Abstraction of above 2 functions, returns tuple with min and max
def get_plot_extremes(data, desired_test, num_of_sites):
    minimum_test = 0
    maximum_test = 1
    temp = 0
    not_found = True
    while not_found:
        if (data[temp].split("|")[1] == desired_test[0]):
            minimum_test = float(data[temp].split("|")[13])
            maximum_test = float(data[temp].split("|")[14])
            not_found = False
        temp = temp + num_of_sites
    return [minimum_test, maximum_test]


# Plots the results of all sites from one test
def plot_full_test_trend(test_data, minimum, maximum):

    # Plots each site one at a time
    for i in range(0, len(test_data)):
        plot_single_site_trend(test_data[i], minimum, maximum)

    # Plots the minimum and maximum barriers
    plt.plot(range(0, len(test_data[0])), [minimum] * len(test_data[0]), color="red", linewidth=3.0)
    plt.plot(range(0, len(test_data[0])), [maximum] * len(test_data[0]), color="red", linewidth=3.0)

    # My feeble attempt to get pretty dynamic limits
    expand = max([abs(minimum), abs(maximum)])
    plt.ylim(ymin= minimum - abs(0.05 * expand))
    plt.ylim(ymax= maximum + abs(0.05 * expand))



# Plots a single site's results
def plot_single_site_trend(site_data, min, max):
    plt.plot(range(0,len(site_data)), site_data)


# Creates an array of arrays that has the raw data for each test site in one particular test
# Given the integer number of sites under test and the Array result from ptr_extractor for a certain test num + name,
#   expect a 2D array with each row being the reran test results for each of the sites in a particular test
def single_test_data(num_of_sites, extracted_ptr):

    # Me being bad at initializing arrays again, hush
    single_test = [np.zeros(int(len(extracted_ptr) / num_of_sites))]

    # Runs through once for each of the sites in the test, incrementing by 1
    for i in range(0, num_of_sites):

        single_site = []

        # Runs through once for each of the loops of the test, incrementing by the number of test sites until all test
        # loops are covered for the individual testing site. The incremented i offsets it so that it moves on to the
        # next testing site
        for j in range(i, len(extracted_ptr), num_of_sites):

            single_site = np.append(single_site, float(extracted_ptr[j, 5]))

        single_test = np.vstack([single_test, single_site])

    # Deletes that initialized row because I suck and don't know how numpy works
    single_test = np.delete(single_test, 0, 0)

    return single_test



# Integer, Parsed List of Strings (PTR specifically), tuple -> Array
# It grabs the data for a certain test in the PTR data and turns that specific test into an array of arrays
def ptr_extractor(num_of_sites, data, test_number):

    # Initializes an array of the data from one of the tests for all test sites
    ptr_array_test = np.zeros(len(data[0].split("|")))

    # Finds where in the data to start looking for the test in question
    starting_index = 0
    for i in range(0, len(data), num_of_sites):
        if (data[i].split("|")[1] == test_number[0]) and (data[i].split("|")[7] == test_number[1]):
            starting_index = i
            for j in range(starting_index, (starting_index + num_of_sites)):
                ptr_array_test = np.vstack([ptr_array_test, data[j].split("|")])

    # Appends each row of the test's data to cover the entire test and nothing more
    # for j in range (starting_index, (starting_index + num_of_sites)):
    #     ptr_array_test = np.vstack([ptr_array_test,data[j].split("|")])

    # Maybe I just suck at initializing arrays in numpy but I couldn't be bothered to do it without just creating an
    # array full of zeros first and then just removing it later.
    ptr_array_test = np.delete(ptr_array_test, 0, 0)
    ptr_array_test = np.delete(ptr_array_test, 0, 1)

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