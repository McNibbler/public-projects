###################################################
# ATE Data Reader Python Edition                  #
# Version 0.1                                     #
#                                                 #
# March 1, 2018                                   #
# Thomas Kaunzinger                               #
# XCerra Corp.                                    #
#                                                 #
# References:                                     #
# PySTDF Library                                  #
# My crying soul because there's no documentation #
###################################################

# Importing a bunch of stuff that I probably won't even need but we'll just roll with it for now
from __future__ import print_function


from pystdf.IO import *
from pystdf.Writers import *

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


gzPattern = re.compile('\.g?z', re.I)
bz2Pattern = re.compile('\.bz2', re.I)

###################################################

wd = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(wd,"Data\\data.std")

print(filepath)

###################################################

# lmfao i just took this from the stdf2text script and im trying to change it so it works but there's no documentation
# im crying inside and out send help
def process_file(filename):

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

    # Opens otherwise
    else:
        f = open(filename, 'rb')

    p = Parser(inp=f, reopen_fn=reopen_fn)
    p.addSink(XmlWriter())
    p.parse()
    f.close()

    # if len(fnames) < 2:
    #     p.addSink(TextWriter())
    #     p.parse()
    # else:
    #     with open(fnames, 'w') as fout:
    #         p.addSink(TextWriter(stream=fout))
    #         p.parse()


###################################################


process_file(filepath)