#!/usr/bin/env python
#
# Name: coverage_graph.py
# Author: Reece Chae
# Description: 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import sys

bed_files = glob.glob("*.bed")
zero_depth_counts = {}
for bed_file in bed_files:
    df = pd.read_csv(bed_file, sep='\t', names=["chrom", "start", "end", "coverage"])
    for _, row in df.iterrows():
        key = (row["chrom"], row["start"], row["end"])
        zero_depth_counts[key] = zero_depth_counts.get(key,0) + 1
plot_data = pd.DataFrame(
        [(k[0], k[1], v) for k, v in zero_depth_counts.items()],
        columns=["chrom","position","count"]
        )
plot_data = plot_data.sort_values(by=["chrom","position"])
plt.figure(figsize=(12, 6))
for chrom in plot_data["chrom"].unique():
    subset = plot_data[plot_data["chrom"] == chrom]
    plt.plot(subset["position"], subset["count"], label=f"Chr {chrom}")
plt.xlabel("Genomic Position")
plt.ylabel("Number of BED Files with Depth 0")
plt.title("Coverage Dropout Across Multiple BED Files")
plt.legend()
plt.savefig('result.png')
sys.exit()