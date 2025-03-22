#!/usr/bin/env python
#
# Name: coverage_graph_zero.py
# Author: Reece Chae
# Description: 
# Notes: For Linux, using PyQt Environment, you may need to set the QT_QPA_PLATORM variable in your shell.  
# Setting this variable to "offscreen" allows PyQt apps to run in a headless environment.  
#               # export QT_QPA_PLATFORM=offscreen

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob

bed_files = glob.glob("*.bed")
zero_depth_counts = {}
chromosome_ranges = {}

for file in bed_files:
    df = pd.read_csv(file, sep="\t", header=None, names=["chrom", "start", "end", "depth"])
    for _, row in df.iterrows():
        for pos in range(row["start"], row["end"] + 1):
            if row["chrom"] not in chromosome_ranges:
                chromosome_ranges[row["chrom"]] = {"min": pos, "max": pos}
            else:
                chromosome_ranges[row["chrom"]]["min"] = min(chromosome_ranges[row["chrom"]]["min"], pos)
                chromosome_ranges[row["chrom"]]["max"] = max(chromosome_ranges[row["chrom"]]["max"], pos)
            if row["depth"] == 0:
                zero_depth_counts[(row["chrom"], pos)] = zero_depth_counts.get((row["chrom"], pos), 0) + 1
plot_data = []
x_position_index = 0
for chrom in sorted(chromosome_ranges.keys()):
    min_pos = chromosome_ranges[chrom]["min"]
    max_pos = chromosome_ranges[chrom]["max"]
    for pos in range(0, max_pos + 1):
        count = zero_depth_counts.get((chrom, pos), 0)
        plot_data.append((chrom, pos, count, x_position_index, chrom))
        x_position_index += 1  
plot_data = pd.DataFrame(plot_data, columns=["chrom", "position", "count", "x_position", "chrom_color"])
num_chromosomes = len(plot_data['chrom'].unique())
cmap = plt.cm.viridis
colors = [cmap(i / num_chromosomes) for i in range(num_chromosomes)]
chrom_colors = {chrom: colors[i] for i, chrom in enumerate(plot_data['chrom'].unique())}
plt.figure(figsize=(12, 6))
for chrom in plot_data['chrom'].unique():
    chrom_data = plot_data[plot_data['chrom'] == chrom]
    plt.scatter(chrom_data['x_position'], chrom_data['count'], s=10, color=chrom_colors[chrom])
plt.xlabel("Chromosome")
plt.ylabel("Number of BED Files with Depth 0")
plt.title("Positions with Zero Depth Across BED Files")
chromosomes = sorted(chromosome_ranges.keys())
tick_positions = [plot_data[plot_data['chrom'] == chrom].iloc[-1]['x_position'] for chrom in chromosomes]
plt.xticks(ticks=tick_positions, labels=chromosomes, rotation=90, fontsize=8)
plt.tight_layout()
plt.savefig('coverage_graph_zero.png')
plt.close()