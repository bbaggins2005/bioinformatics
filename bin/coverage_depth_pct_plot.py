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
print(df_parquet_data.compute())