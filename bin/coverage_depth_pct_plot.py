#!/usr/bin/env python
#
# Name: coverage_depth_pct_plot.py
# Author: Reece Chae
# Description:

import matplotlib.pyplot as plt
import dask.dataframe as dd
import dask.array as da
import sys
import os
import re
import glob
import argparse
import itertools
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

os.environ["QT_QPA_PLATFORM"] = "offscreen"

def has_subdir(dir):
    return any(os.path.isdir(os.path.join(dir, subdir)) for subdir in os.listdir(dir))

def process_bed_file(file, chromosome, parquet_dir):
    df = dd.read_csv(file, sep="\t", header=None, names=["chrom", "start", "end", "depth"])
    df_chrom = df[df["chrom"] == chromosome ]
    df_chrom["name"] = re.sub(r"\.bed$", "", os.path.basename(file), flags=re.IGNORECASE)
    parquet_bed_file_dir = os.path.join(parquet_dir, f"{os.path.basename(file)}.parquet")
    df_chrom.to_parquet(parquet_bed_file_dir, engine="pyarrow", write_index=False)

def plot_fraction_depth(parquet_dir, plotfilename):
    parquet_strip_dir = parquet_dir.rstrip('/\\')
    df_parquet_data = dd.read_parquet(parquet_strip_dir + '/**/*.parquet', engine="pyarrow", recursive=True)
    series_dict = defaultdict(lambda: defaultdict(int))
    max_positions = defaultdict(int)
    for partition in df_parquet_data.to_delayed():
        pdf = partition.compute()
        for name, chrom, start, end, depth in zip(pdf["name"], pdf["chrom"], pdf["start"], pdf["end"], pdf["depth"]):
            for pos in range(start, end + 1):
                series_dict[(name, chrom)][pos] = depth
                max_positions[(name, chrom)] = max(max_positions[(name, chrom)], pos)
    for (name, chrom), max_pos in max_positions.items():
       for pos in range(1, max_pos + 1):
            if pos not in series_dict[(name, chrom)]:
                series_dict[(name, chrom)][pos] = 0
    plot_data = {}
    for (name, chrom), depths in series_dict.items():
        depth_array = da.from_array(list(depths.values()), chunks=len(depths))
        depth_counts = depth_array.compute()
        unique, counts = da.unique(depth_array, return_counts=True)
        depth_counts = dict(zip(unique.compute(), counts.compute()))
        total_counts = sum(depth_counts.values())
        depth_counts = {k: v / total_counts for k, v in depth_counts.items()}
        sorted_depths = sorted(depth_counts.items())
        accumulated_fraction = 0.0
        accumulated_depth_counts = {}
        for depth, fraction in sorted_depths:
            accumulated_fraction += fraction
            accumulated_depth_counts[depth] = accumulated_fraction
        plot_data[(name, chrom)] = accumulated_depth_counts
    plt.figure(figsize=(10, 6))
    for (name, chrom), accumulated_depth_counts in plot_data.items():
        depths_x = list(accumulated_depth_counts.keys())
        fractions_y = list(accumulated_depth_counts.values())
        plt.plot(depths_x, fractions_y, marker='o', linestyle='-', label=f"{name} ({chrom})")
        threshold = 20
        if args.threshold:
            threshold = args.threshold
        plt.axvline(x=threshold, color='red', linestyle='--', linewidth=2)
    plt.xlabel("Coverage Depth")
    plt.ylabel("Accumulated Fraction of Observed Positions")
    plt.title("Accumulated Coverage Depth Distribution for " + chrom)
    plt.legend()
    plt.grid(True)
    plotfilename += '.png'
    plt.savefig(plotfilename)
    plt.close()

def main(args):
    os.makedirs(args.parquetdir, exist_ok=True)
    if not args.output and not ( args.input or args.directory ):
        print("erro: you must specify either --output or (the --input or --directory) switches")
        sys.exit(10)
    if args.directory or args.input:
        if not args.chromosome:
            print("erro: --chromosome switch is required if assessing bed file (with -i or -d switches)")
            sys.exit(11)
        else:
            if args.directory:
                bedfiledir = args.directory + '/*.bed'
                bed_files = glob.glob(bedfiledir)
            elif args.input:
                bed_files = [ args.input ] 
            with ThreadPoolExecutor(max_workers=8) as executor:
                executor.map(process_bed_file, bed_files, itertools.repeat(args.chromosome), itertools.repeat(args.parquetdir))
    if args.output:
        if has_subdir(args.parquetdir):
            plot_fraction_depth(args.parquetdir, args.output)
        else:
            print(f"erro: parquet directory {args.parquetdir} is empty")
            sys.exit(12)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type = str, required = False, help = "specify bed file to assess")
    parser.add_argument("--directory", type = str, required = False, help = "specify directory of bed files to assess")
    parser.add_argument("--parquetdir", type = str, required = True, help = "(required) specify directory to store intermediate data for plotting")
    parser.add_argument("--chromosome", type = str, required = False, help = "specify chromosome to filter")
    parser.add_argument("--output", type = str, required = False, help = "specify output png file name")
    parser.add_argument("--threshold", type = int, required = False, help = "specify depth value of threshold line")
    args = parser.parse_args()
    main(args)
    sys.exit()