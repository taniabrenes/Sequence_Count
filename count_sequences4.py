
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 10:02:04 2017

@author: tbrenes

Input read1 + read2 of a fastq sequence, or a tab delimited file.
"""

import gzip
import sys
import argparse

def read_1fastq_sequence(ri):
        ID = ri.readline().strip()
        Seq = ri.readline().strip()
        nn = ri.readline().strip()
        qc = ri.readline().strip()
        return [ID, Seq, nn, qc]

parser = argparse.ArgumentParser(description = 'Count sequences in a fastq file')
parser.add_argument("reads", nargs = '*', default = sys.stdin,
                    help = "File names for the fastq sequences")
parser.add_argument("-q", "--quiet", action = "store_false",
                  help = "Do not print sequence to screen.", 
                  dest = "verbose", default = True)
parser.add_argument("-o", "--output", action = "store",
                  help = "Save sequence count to a text file.", 
                  dest = "outfile", default = "none")

args = parser.parse_args()

if type(args.reads) == file:
    r1 = args.reads

    ## Check if stdin file is already tab delimited 
    l1 = r1.readline().strip()
    n = 1
    
    if len(l1.split('\t')) > 1:
        for line in r1:
            n += 1
            if args.verbose:
                sys.stdout.write(line)
    else:
        sys.exit("Stdin input must be tab delimited\n")

##  If there are file names in reads, open input files
##  and convert to tab delimited.
else:
    r1f = args.reads[0]
    if r1f.split('.')[-1] == 'gz':
        r1 = gzip.open(r1f)
    else:
        r1 = open(r1f)
    
    r2f = args.reads[1]
    if r1f.split('.')[-1] == 'gz':
        r2 = gzip.open(r2f)
    else:
        r2 = open(r1f)

    # Check data.
    (ID1, Seq1, nn1, qc1) = read_1fastq_sequence(r1)
    (ID2, Seq2, nn2, qc2) = read_1fastq_sequence(r2)
    
    # checks for the symbol + to make sure files are fastq format
    if nn1 != "+" or nn2 != "+":
        sys.exit( "Read files must be in fastq format.\n")

    # compare the seq id of r1 and r1 to make sure they match. 
    if ID1[:39] != ID2[:39]:
        sys.exit("Sequence IDs do not match between reads.\n")

    r1.seek(0)
    r2.seek(0)
    
    n = 0

    # an open loop to read r1 and r2
    while True:
        
        (ID1, Seq1, nn1, qc1) = read_1fastq_sequence(r1)
        (ID2, Seq2, nn2, qc2) = read_1fastq_sequence(r2)
        
        if not ID1:
            break
    
        n += 1
        if args.verbose:
            line  = '\t'.join([ID1, Seq1, qc1, Seq2, qc2 + "\n"])
            sys.stdout.write( line )

# output the sequence count 
if args.outfile != "none":
    out = open (args.outfile, "a") 
    out.write("\nCount = %s\n" % n)
    out.close()
else:
    sys.stderr.write("\nTotal number of sequences is: %s\n" % n)

