#!/usr/bin/env python
#
# Name: coverage_depth_pctplot.py
# Author: Reece Chae
# Description:

import matplotlib.pyplot as plt
import dask.dataframe as dd
import re
import glob
from concurrent.futures import ThreadPoolExecutor

chromosome = "chr1"

def process_bed_file(file):
    df = dd.read_csv(file, sep="\t", header=None, names=["chrom", "start", "end", "depth"])
    df_chrom = df[df["chrom"] == chromosome ]
    df_chrom["name"] = re.sub(r"\.bed$", "", file, flags=re.IGNORECASE)
    return df_chrom

bed_files = glob.glob("*.bed")
with ThreadPoolExecutor(max_workers=8) as executor:
    results = executor.map(process_bed_file, bed_files)

for df_chrom in results:
    for name, chrom, start, end, depth in zip(df_chrom["name"], df_chrom["chrom"], df_chrom["start"], df_chrom["end"], df_chrom["depth"]):
        print(name, chrom, start, end, depth) 