#!/usr/bin/env python
#
# Name: coverage_depth_pct_plot.py
# Author: Reece Chae
# Description:

import matplotlib.pyplot as plt
import dask.dataframe as dd
import os
import re
import glob
from concurrent.futures import ThreadPoolExecutor

chromosome = "chr1"
parquet_dir = "tmp/01"
os.makedirs(parquet_dir, exist_ok=True)

def process_bed_file(file):
    df = dd.read_csv(file, sep="\t", header=None, names=["chrom", "start", "end", "depth"])
    df_chrom = df[df["chrom"] == chromosome ]
    df_chrom["name"] = re.sub(r"\.bed$", "", file, flags=re.IGNORECASE)
    parquet_bed_file_dir = os.path.join(parquet_dir, f"{os.path.basename(file)}.parquet")
    df_chrom.to_parquet(parquet_bed_file_dir, engine="pyarrow", write_index=False)

bed_files = glob.glob("*.bed")
with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(process_bed_file, bed_files)
df_parquet_data = dd.read_parquet(parquet_dir + '/**/*.parquet', engine="pyarrow", recursive=True)
series_dict = {}
for partition in df_parquet_data.to_delayed():
    pdf = partition.compute()
    for name, chrom, start, end, depth in zip(pdf["name"], pdf["chrom"], pdf["start"], pdf["end"], pdf["depth"]):
        if (name, chrom) not in series_dict:
            series_dict[(name, chrom)] = []
        positions_count = end - start + 1
        series_dict[(name, chrom)].extend([depth] * positions_count)
        print(series_dict[(name,chrom)])
        print(name, chrom, start, end, depth, "here is position count", positions_count, "for name and chrom", name, chrom, series_dict[(name,chrom)])