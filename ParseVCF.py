#!/usr/bin/env python
#
# Name: ParseVCF.py
# Author: Reece Chae
# Description: This program should parse an unphased VCF file and output 8 files (4 per scenario)
# In one scenario, A7 is healthy, in the other, A7 and A1 are healthy
# The four files will be the segregated set, non-segregated set, a missing set, and a family-missing set
# Notes: unfinished

import vcf
import sys, os
import random
import string

def grab_header_from_vcf(vcfname, header_filename):
    prefix = "##"
    with open(vcfname, 'r') as file:
        with open(header_filename, 'w') as header_file:
            for line in file:
                if line.startswith(prefix):
                    header_file.write(line)
            colname_line = '#CHROM\tPOS\tREF\tALT\tA1\tA2\tA3\tA4\tA5\tA6\tA7\n'
            #work on
            header_file.write(colname_line)

def cleanup_tmpfiles(header_filename):
    os.remove(header_filename)

def main():
    vcfname = 'example.vcf'  
    header_filename = '.ParseVCF_header-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    grab_header_from_vcf(vcfname, header_filename)
    vcf_reader = vcf.Reader(open('example.vcf','r'))
    for record in vcf_reader:
        samples_dict = {}
        for sample in record.samples:
            samples_dict[sample.sample] = sample['GT']
        

# do the criteria, if else

# within this loop block, write the 4 output 






    cleanup_tmpfiles(header_filename)
    sys.exit()







if __name__ == "__main__":
    main()