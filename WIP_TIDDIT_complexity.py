import sys
import argparse
import os
import subprocess
import time
import csv

#example command: tiddit --sv   --bam /home/brendonleah/HG002.sorted_25pct.bam   --ref /home/brendonleah/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna   --prefix /home/brendonleah/tiddit_test

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

prefix = "tiddit_calls"
time_output = "tiddit_time.txt"


command = ["tiddit","--sv", "--bam", infile, "--ref", reference,"--prefix", prefix]

start = time.perf_counter()

result = subprocess.run(
    ["/usr/bin/time", "-v", "-o", time_output] + command,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

runtime = time.perf_counter() - start

# Extract peak memory from GNU time output
peak_memory = "NA"

with open(time_output, "r") as timefile:
    for line in timefile:
        if "Maximum resident set size (kbytes)" in line:
            peak_memory = round(
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
        "TIDDIT", infile, reference,
        round(runtime, 3), peak_memory, result.returncode
    ])
