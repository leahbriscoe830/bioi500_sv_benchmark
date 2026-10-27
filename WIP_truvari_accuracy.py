import subprocess
import os
import sys
import argparse

# Function to parse command-line arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="Run manta and record runtime and peak memory in a txt."
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
input_dir = arguments.input # '/home/brendonleah/data/HG002.sorted.bam' # maybe this should reference a directory with all the downsampled BAMs, then we can iterate in this script
ref_fa = arguments.reference # '/home/brendonleah/data/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna'
truth_vcf = arguments.truth # '/home/brendonleah/data/HG002_GRCh38_v5.0q_stvar.vcf.gz'

for root, dirs, files in os.walk(input_dir):
    for test_vcf in files:
        # Run truvari on input vcf: 
        subprocess.run(['truvari', 'bench', '-b', test_vcf, '-c', truth_vcf, '-f', ref_fa, '-o', f'results/truvari/'])