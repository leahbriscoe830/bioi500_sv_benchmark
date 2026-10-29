import sys
import argparse
import os
import csv
import subprocess
import time

# example command in terminal :  python WIP_Delly_complexity.py   -i /home/brendonleah/HG002.sorted_25pct.bam   -r /home/brendonleah/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna   -o /home/brendonleah/benchmark_results.csv
# Function to parse command-line arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="Run TIDDIT and record runtime and peak memory in a CSV."
    )
    parser.add_argument(
        "-i", "--input",
        help="Input BAM/CRAM file",
        required=True
    )
    parser.add_argument(
        "-o", "--output",
        help="Output CSV file for benchmark results",
        required=True
    )
    parser.add_argument(
        "-r", "--reference",
        help="Reference genome FASTA file",
        required=True
    )
    return parser.parse_args(args)


# Retrieve command-line arguments
arguments = check_arg(sys.argv[1:])
infile = arguments.input
outfile = arguments.output
reference = arguments.reference

variant_output = "delly_calls.bcf"
time_output = "delly_time.txt"

command = ["delly", "sr", "-g", reference,"-o", variant_output,infile]
# Measure wall-clock runtime and GNU time resource usage
start = time.perf_counter()

with open(time_output, "w") as timefile:
    result = subprocess.run(
        ["/usr/bin/time", "-v", "-o", time_output] + command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

runtime = time.perf_counter() - start

# Extract peak memory from GNU time output
peak_memory_mb = "NA"

with open(time_output, "r") as timefile:
    for line in timefile:
        if "Maximum resident set size (kbytes)" in line:
            peak_memory_mb = round(
                int(line.split(":")[-1].strip()) / 1024, 2
            )

# Write results to CSV; create headers only if needed
write_header = (
    not os.path.exists(outfile) or os.path.getsize(outfile) == 0
)

with open(outfile, "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    if write_header:
        writer.writerow([
            "tool", "input", "reference",
            "runtime_seconds", "peak_memory_mb", "exit_code"
        ])

    writer.writerow([
        "Delly", infile, reference,
        round(runtime, 3), peak_memory_mb, result.returncode
    ])


