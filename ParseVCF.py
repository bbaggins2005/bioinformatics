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
import sys, os, re, argparse

def check_missing(samples_GT):
    # for polyploid organisms or unique cases
    # missingpattern = re.compile(r'^\.([/|]\.){1,2}$')
    missingpattern = re.compile(r'^\.[/|]\.$') 
    for GT in samples_GT.values():
        if not missingpattern.search(GT):
            return False
    return True

def check_segregated(healthy_samples_GT, unhealthy_samples_GT):
    healthy_GT_values = set(healthy_samples_GT.values())
    unhealthy_GT_values = set(unhealthy_samples_GT.values())
    return healthy_GT_values.isdisjoint(unhealthy_GT_values)

def pedigree_healthy(pedigree_file):
    unaffected = []
    with open(pedigree_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        fields = line.split()
        if fields[5] == '1':
            unaffected.append(fields[1])
    return unaffected

def main(args):
    if os.path.exists(args.file):
        vcfname = args.file
    else:
        print(f"The file '{args.file}' does not exist.")
        sys.exit(10)

    if args.healthy:
        healthy_samples = args.healthy.split(',')
    elif os.path.exists(args.pedigree):
        healthy_samples = pedigree_healthy(args.pedigree)
    else:
        print(f"Must specify --healthy or --pedigree switch")
        sys.exit(11)

    outputvcfname = vcfname.replace('.vcf', '')
    outputvcfname += '_healthy_' + '_'.join(healthy_samples) + '_'
   
    vcf_reader = vcf.Reader(open(vcfname,'r'))
    vcf_writer1 = vcf.Writer(open(outputvcfname + 'missing.vcf', 'w'), vcf_reader)
    vcf_writer2 = vcf.Writer(open(outputvcfname + 'familymissing.vcf', 'w'), vcf_reader)
    vcf_writer3 = vcf.Writer(open(outputvcfname + 'segregated.vcf', 'w'), vcf_reader)
    vcf_writer4 = vcf.Writer(open(outputvcfname + 'nonsegregated.vcf', 'w'), vcf_reader)

    for record in vcf_reader:
        samples_dict = {}
        for sample in record.samples:
            samples_dict[sample.sample] = sample['GT']
        unhealthy_samples_GT = {key: value for key, value in samples_dict.items() if key not in healthy_samples}
        healthy_samples_GT = {key: value for key, value in samples_dict.items() if key in healthy_samples}
        ismissing = check_missing(healthy_samples_GT)
        isfamilymissing = check_missing(unhealthy_samples_GT)
        issegregated = check_segregated(healthy_samples_GT, unhealthy_samples_GT)

        if ismissing:
            vcf_writer1.write_record(record)
        elif isfamilymissing:
            vcf_writer2.write_record(record)
        elif issegregated:
            vcf_writer3.write_record(record)
        else:
            vcf_writer4.write_record(record)

    vcf_writer1.close()
    vcf_writer2.close()
    vcf_writer3.close()
    vcf_writer4.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type = str, required = True, help = "specify VCF file to be parsed")
    parser.add_argument("--healthy", type = str, required = False, help = "specify healthy samples (delimited by ,), takes precedence over --pedigree switch")
    parser.add_argument("--pedigree", type = str, required = False, help = "specify pedigree file name (.ped or .fam), unless healthy samples listed")
    args = parser.parse_args()
    main(args)
    sys.exit()