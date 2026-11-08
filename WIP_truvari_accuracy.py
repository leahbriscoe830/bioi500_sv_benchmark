import subprocess
import os
import sys
import argparse

# Function to parse command-line arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="Benchmark specified vcf files using truvari."
    )
    parser.add_argument(
        "-i", "--input",
        help="Location of input vcf files",
        required=True
    )
    parser.add_argument(
        "-r", "--reference",
        help="Reference genome FASTA file",
        required=True
    )
    parser.add_argument(
        "-t", "--truth",
        help="Truth vcf file",
        required=True
    )
    return parser.parse_args(args)

# Retrieve command-line arguments
arguments = check_arg(sys.argv[1:])
input_dir = arguments.input 
ref_fa = arguments.reference # '/home/brendonleah/data/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna'
truth_vcf = arguments.truth # '/home/brendonleah/data/HG002_GRCh38_v5.0q_stvar.vcf.gz'

for root, dirs, files in os.walk(input_dir):
    for test_vcf in files:
        # Run truvari on input vcf: 
        subprocess.run(['truvari', 'bench', '-b', test_vcf, '-c', truth_vcf, '-f', ref_fa, '-o', f'results/truvari/'])