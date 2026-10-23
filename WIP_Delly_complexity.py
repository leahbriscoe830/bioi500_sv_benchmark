import sys
import argparse
import os
import subprocess
import time


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

command = ["delly", "call","-g", reference,"-o", variant_output,infile]
# Measure wall-clock runtime and GNU time resource usage
start = time.perf_counter()

peak_memory_mb = None

