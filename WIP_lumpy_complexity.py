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
    return parser.parse_args(args)

# Retrieve command-line arguments
arguments = check_arg(sys.argv[1:])
input_bam = arguments.input # '/home/brendonleah/data/HG002.sorted.bam' # maybe this should reference a directory with all the downsampled BAMs, then we can iterate in this script

subsamples = [0.01, 0.02, 0.03, 0.04, 0.05] # exact downsample fractions TBD
times = [] # measure time across 5 subsamples of input bam
mem_usage = [] # measure memory across 5 subsamples of input bam

for frac in subsamples:
    # Downsample input bam file: samtools view -b -s 0.01 -o downsampled.bam input.bam
    #subprocess.call(['samtools', 'view', '-b', '-s', str(frac), '-o', '{}_input.bam'.format(frac), input_bam])

    # Add dummy read group header: samtools addreplacerg -r '@RG\tID:sample1\tLB:lib1\tPL:ILLUMINA\tSM:sample1' -o output.bam input.bam
    subprocess.call(['samtools', 'addreplacerg', '-r', '@RG\tID:sample1\tLB:lib1\tPL:ILLUMINA\tSM:sample1', '-o', 'results/lumpy/{}_input_rg.bam'.format(frac), input_bam])

    # Index new bam file: samtools index input.bam
    subprocess.call(['samtools', 'index', 'results/lumpy/{}_input_rg.bam'.format(frac)])

    start_time = time.time()

    # Run lumpy: lumpyexpress -B my.bam -o output.vcf
    proc = subprocess.Popen(['lumpyexpress', '-B', 'results/lumpy/{}_input_rg.bam'.format(frac), '-o', 'lumpy_acc.vcf'])

    # Get peak memory for lumpyexpress process
    process = psutil.Process(proc.pid)
    peak_memory = 0

    while proc.poll() is None:
        memory = process.memory_info().rss
        if memory > peak_memory:
                peak_memory = memory
        time.sleep(0.1)

    # time complexity lumpy
    end_time = time.time()
    times.append(end_time - start_time)

    # memory complexity lumpy
    mem_usage.append(peak_memory / (1024.0 ** 2)) # convert to MB

# Write complexity data to output file
with open('lumpy_complexity.txt', 'w') as f:
    for i in range(5):
        f.write("{}: {}, {}\n".format(subsamples[i], times[i], mem_usage[i]))