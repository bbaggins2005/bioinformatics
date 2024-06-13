#!/usr/bin/env python
#
# Name: ParseVCF.py
# Author: Reece Chae
# Description: This program should parse an unphased VCF file and output 8 files (4 per scenario)
# In one scenario, A7 is healthy, in the other, A7 and A1 are healthy
# The four files will be the segregated set, non-segregated set, a missing set, and a family-missing set
#
# Notes:
#   1) quotechar error: Project Issue #6.  Reference: https://github.com/dridk/PyVCF3/issues/6
#   quotechar is unused when quoting=csv.QUOTE_NONE is used. To remedy, delete passing quotechar when invoking csv.writer
#   line 776 of parser.py (quotechar = "")
#

import vcf
import sys, os, re, random, string

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

def check_missing(samples_GT):
    # for polyploid organisms or unique cases
    # missingpattern = re.compile(r'^\.([/|]\.){1,2}$')
    missingpattern = re.compile(r'^\.[/|]\.$') 
    for GT in samples_GT.values():
        if not missingpattern.search(GT):
            return False
    return True

def main():
    vcfname = 'example.vcf' 
    healthy_samples = [ 'A1','A7' ]
    outputvcfname = vcfname.replace('.vcf', '')
    outputvcfname += '_healthy_' + '_'.join(healthy_samples) + '_'
    missingvcfname = outputvcfname + 'missing.vcf'

    header_filename = '.ParseVCF_header-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    grab_header_from_vcf(vcfname, header_filename)
    vcf_reader = vcf.Reader(open(vcfname,'r'))
    vcf_writer1 = vcf.Writer(open('test.vcf', 'w'), vcf_reader)
 #   vcf_writer2 = vcf.Writer(open('/dev/null', 'w'), vcf_reader)
#    vcf_writer3 = vcf.Writer(open('/dev/null', 'w'), vcf_reader)
 #   vcf_writer4 = vcf.Writer(open('/dev/null', 'w'), vcf_reader)
    sys.exit()

    for record in vcf_reader:
        samples_dict = {}
        for sample in record.samples:
            samples_dict[sample.sample] = sample['GT']
        unhealthy_samples_GT = {key: value for key, value in samples_dict.items() if key not in healthy_samples}
        healthy_samples_GT = {key: value for key, value in samples_dict.items() if key in healthy_samples}
        ismissing = check_missing(healthy_samples_GT)
        print(healthy_samples_GT)
        print(ismissing)


# do the criteria, if else

# within this loop block, write the 4 output 






    cleanup_tmpfiles(header_filename)
    sys.exit()







if __name__ == "__main__":
    main()