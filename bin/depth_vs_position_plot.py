#!/usr/bin/env python
#
# Name: depth_vs_position_plot.py
# Author: Reece Chae
# Description:

import matplotlib.pyplot as plt
import dask.dataframe as dd
import sys
import os
import re
import argparse
from collections import defaultdict

os.environ["QT_QPA_PLATFORM"] = "offscreen"

def read_bed_file(file, chromosome):
    df = dd.read_csv(file, sep="\t", header=None, names=["chrom", "start", "end", "depth"])
    df_chrom = df[df["chrom"] == chromosome ]
    df_chrom["name"] = re.sub(r"\.bed$", "", file, flags=re.IGNORECASE)
    return df_chrom

def plot_depth_position(df_chrom, plotfilename):
    series_dict = defaultdict(lambda: defaultdict(int))
    max_positions = defaultdict(int)
    for name, chrom, start, end, depth in zip(df_chrom["name"], df_chrom["chrom"], df_chrom["start"], df_chrom["end"], df_chrom["depth"]):
        for pos in range(start, end + 1):
            series_dict[(name, chrom)][pos] = depth
            max_positions[(name, chrom)] = max(max_positions[(name, chrom)], pos)
    for (name, chrom), max_pos in max_positions.items():
       for pos in range(1, max_pos + 1):
            if pos not in series_dict[(name, chrom)]:
                series_dict[(name, chrom)][pos] = 0
    plt.figure(figsize=(10, 6))
    for (name, chrom), pos_and_depths in series_dict.items():
        positions_x = list(pos_and_depths.keys())
        x = sorted(positions_x)
        y = [pos_and_depths[k] for k in x]
        print("depth y", y)
        print("portion x", x)
        plt.plot(x, y, marker='o', linestyle='-', label=f"{name} (chrom)")
    plt.xlabel("Position")
    plt.ylabel("Depth")
    plt.title("Depth Position Plot for " + chrom)
    plt.legend()
    plt.grid(True)
    plotfilename += '.png'
    plt.savefig(plotfilename)
    plt.close()

def main(args):
    df_chrom = read_bed_file(args.file, args.chromosome)
    plot_depth_position(df_chrom, args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type = str, required = True, help = "(required) bed file")
    parser.add_argument("--chromosome", type = str, required = True, help = "(required) chromosome to plot")
    parser.add_argument("--output", type = str, required = True, help = "(required) specify output png file name")
    args = parser.parse_args()
    main(args)
    sys.exit()