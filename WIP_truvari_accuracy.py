import subprocess
import os
import sys
import argparse

# Example: python WIP_truvari_accuracy.py -i test_vcfs/ -r /home/brendonleah/data/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna -t data/HG002_GRCh38_v5.0q_chr20.vcf.gz -b data/HG002_GRCh38_v5.0q_stvar.benchmark.bed
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
    parser.add_argument(
        "-b", "--bed",
        help="Benchmark bed file",
        required=True
    )
    return parser.parse_args(args)

# Retrieve command-line arguments
arguments = check_arg(sys.argv[1:])
input_dir = arguments.input 
ref_fa = arguments.reference # '/home/brendonleah/data/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna'
truth_vcf = arguments.truth # '/home/brendonleah/data/HG002_GRCh38_v5.0q_stvar.vcf.gz'
bench_bed = arguments.bed # '/home/brendonleah/data/bioi500_sv_benchmark/data/HG002_GRCh38_v5.0q_stvar.benchmark.bed'

for test_vcf in os.listdir(input_dir):
    if test_vcf.endswith('pct.vcf.gz'):

        filename = os.path.splitext(os.path.basename('{}{}'.format(input_dir, test_vcf)))[0] #manta_25pct.vcf
        # Get subsample fraction
        tool_frac = filename.split('.') # manta_25pct

        # Run truvari on input vcf: 
        subprocess.run(['truvari', 'bench', '-b', truth_vcf, '-c', f'{input_dir}/{test_vcf}', '-f', ref_fa, '--includebed', bench_bed, '-o', f'results/truvari/{tool_frac[0]}/'])