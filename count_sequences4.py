
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 10:02:04 2017

@author: tbrenes

Input read1 + read2 of a fastq sequence, or a tab delimited file.
"""

import gzip
import sys
import timeit
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-q", "--quite", action = "store_false",
                  help = "don't print sequence to std out", 
                  dest = "verbose", default = True)

(options, args) = parser.parse_args()

pyargs = len(args)

if pyargs == 0:
	r1 = sys.stdin

if pyargs > 0:
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

n = 0

## If file is already tab delimited do a simple count of lines and pipe 
## to console.
ID1 = r1.readline().strip()
r1.seek(0)

if len(ID1.split('\t')) > 1:
    for line in r1:
        n += 1
        if options.verbose:
            sys.stdout.write(line)

## If file is not tab delimited convert to tab before pipe to console.
else:
    while True:
        
        ID1 = r1.readline().strip()
        
        if not ID1:
            break
        
        Seq1 = r1.readline().strip()
        nn1 = r1.readline().strip()
        qc1 = r1.readline().strip()
    
        ID2 = r2.readline().strip()
        Seq2 = r2.readline().strip()
        nn2 = r2.readline().strip()
        qc2 = r2.readline().strip()
    
    # compare the seq id of r1 and r1 to make sure they match. It compares 
    # lines only up to pos 39 because after that there name has the read #
        if ID1[:39] != ID2[:39]:
            break
            print "Sequence IDs do not match between reads\n"
    # checks for the symbol + to make sure files are fastq format
        if nn1 != "+" or nn2 != "+":
            break
            print "Reads file may not be in fastq format\n"
    
        line  = '\t'.join([ID1, Seq1, qc1, Seq2, qc2 + "\n"])
        n += 1
        if options.verbose:
            sys.stdout.write( line )

# output the sequence count on a sepparate file. This is to avoid it going
# into the std out with the sequence

sys.stderr.write("\nTotal number of sequences is: %s\n" % n)
out = open ("Count_Output", "a") 
out.write("\nTotal number of sequences is: %s\n" % n)
out.close()

