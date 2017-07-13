
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 10:02:04 2017

@author: tbrenes

Input read1 + read2 of a fastq sequence, or a tab delimited file.
"""

import gzip
import sys
from optparse import OptionParser

def read_1fastq_sequence(ri):
        ID = ri.readline().strip()
        Seq = ri.readline().strip()
        nn = ri.readline().strip()
        qc = ri.readline().strip()
        return [ID, Seq, nn, qc]

parser = OptionParser()
parser.add_option("-q", "--quite", action = "store_false",
                  help = "Do not print sequence to screen.", 
                  dest = "verbose", default = True)
parser.add_option("-o", "--output", action = "store",
                  help = "Save sequence count to a text file.", 
                  dest = "outfile", default = "none")

(options, args) = parser.parse_args()

pyargs = len(args)

n = 0

if pyargs == 0:
    r1 = sys.stdin

##  If there are file names in args, open input files
else:
    r1f = args[0]
    if r1f.split('.')[-1] == 'gz':
        r1 = gzip.open(r1f)
    else:
        r1 = open(r1f)

    if pyargs == 2:
        r2f = args[1]
        if r1f.split('.')[-1] == 'gz':
            r2 = gzip.open(r2f)
        else:
            r2 = open(r1f)
    else:
        sys.exit("Error: Wrong input. Please enter file names for read 1 and read 2")

## Check if stdin file is already tab delimited 
ID1 = r1.readline().strip()
r1.seek(0)

if len(ID1.split('\t')) > 1:
    for line in r1:
        n += 1
        if options.verbose:
            sys.stdout.write(line)

## If file is not tab delimited convert to tab and pipe to console.
else:
    # Check data. 
    # make sure data is entered as a fastq sequence
    (ID1, Seq1, nn1, qc1) = read_1fastq_sequence(r1)
    (ID2, Seq2, nn2, qc2) = read_1fastq_sequence(r2)
    
    # checks for the symbol + to make sure files are fastq format
    if nn1 != "+" or nn2 != "+":
        sys.exit( "Read files may not be in fastq format.\n")

    # compare the seq id of r1 and r1 to make sure they match. It compares 
    # lines only up to pos 39 because after that there name has the read #
    if ID1[:39] != ID2[:39]:
        sys.exit("Sequence IDs do not match between reads.\n")

    r1.seek(0)
    r2.seek(0)

    # an open loop to read r1 and r2
    while True:
        
        (ID1, Seq1, nn1, qc1) = read_1fastq_sequence(r1)
        (ID2, Seq2, nn2, qc2) = read_1fastq_sequence(r2)
        
        if not ID1:
            break
    
        n += 1
        if options.verbose:
            line  = '\t'.join([ID1, Seq1, qc1, Seq2, qc2 + "\n"])
            sys.stdout.write( line )

# output the sequence count 
if options.outfile != "none":
    out = open (options.outfile, "a") 
    out.write("\nCount = %s\n" % n)
    out.close()
else:
    sys.stderr.write("\nTotal number of sequences is: %s\n" % n)

