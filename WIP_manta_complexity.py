import subprocess
import time
import os
import sys
import psutil
import argparse

# Function to parse command-line arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="Run manta and record runtime and peak memory in a txt."
    )
    parser.add_argument(
        "-i", "--input",
        help="Input BAM/CRAM file",
        required=True
    )
    parser.add_argument(
        "-r", "--reference",
        help="Reference genome FASTA file",
        required=True
    )
    parser.add_argument(
        "-c", "--config_path",
        help="Path to you configManta.py file, located in /home/usr/miniconda3/envs/manta_env/bin",
        required=True
    )
    return parser.parse_args(args)

# Retrieve command-line arguments
arguments = check_arg(sys.argv[1:])
input_bam = arguments.input # '/home/brendonleah/data/HG002.sorted.bam' # maybe this should reference a directory with all the downsampled BAMs, then we can iterate in this script
ref_fa = arguments.reference # 'data/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna'
path_to_config = arguments.config_path # '/home/lbriscoe/miniconda3/envs/manta_env/bin/configManta.py'

subsamples = [0.01, 0.02, 0.03, 0.04, 0.05] # exact downsample fractions TBD
times = [] # measure time across 5 subsamples of input bam
mem_usage = [] # measure memory across 5 subsamples of input bam

for frac in subsamples:
    # Downsample input bam file: samtools view -b -s 0.01 -o downsampled.bam input.bam
    # subprocess.call(['samtools', 'view', '-b', '-s', str(frac), '-o', '{}_input.bam'.format(frac), input_bam])

    # Configure manta: /path/to/manta/bin/configManta.py --bam=input.bam --referenceFasta=reference.fa --runDir=/path/to/manta_somatic_output
    subprocess.call([path_to_config, '--bam', input_bam, '--referenceFasta', ref_fa, '--runDir', 'results/manta/'])

    start_time = time.time()
    
    # Run manta: python /path/to/manta_somatic_output/runWorkflow.py -m local -j 8
    proc = subprocess.Popen(['python', 'results/manta/runWorkflow.py', '-m', 'local']) 

    # Get peak memory for manta workflow process
    process = psutil.Process(proc.pid)
    peak_memory = 0

    while proc.poll() is None:
        memory = process.memory_info().rss
        if memory > peak_memory:
                peak_memory = memory
        time.sleep(0.1)

    # time complexity manta
    end_time = time.time()
    times.append(end_time - start_time)

    # memory complexity manta
    mem_usage.append(peak_memory / (1024.0 ** 2)) # convert to MB

with open('manta_complexity.txt', 'w') as f:
    for i in range(5):
        f.write("{}: {} sec, {} MB\n".format(subsamples[i], times[i], mem_usage[i]))