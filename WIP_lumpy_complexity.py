import subprocess
import time
import os
import sys
import psutil
import argparse
import csv

# Function to parse command-line arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="Run lumpy and record runtime and peak memory in a txt."
    )
    parser.add_argument(
        "-i", "--input",
        help="Directory where input BAM/CRAM subsampled files are located",
        required=True
    )
    return parser.parse_args(args)

# Retrieve command-line arguments
arguments = check_arg(sys.argv[1:])
input_dir = arguments.input

for input_bam in os.listdir(input_dir):
    if input_bam.startswith('HG002.sorted_') and input_bam.endswith('pct.bam'):

        # Get full name for each file (minus extension)
        filename = os.path.splitext(os.path.basename('{}{}'.format(input_dir, input_bam)))[0]

        # Add dummy read group header: samtools addreplacerg -r '@RG\tID:sample1\tLB:lib1\tPL:ILLUMINA\tSM:sample1' -o output.bam input.bam
        subprocess.call(['samtools', 'addreplacerg', '-r', '@RG\tID:sample1\tLB:lib1\tPL:ILLUMINA\tSM:sample1', '-o', 'results/lumpy/{}_rg.bam'.format(filename), '{}{}'.format(input_dir, input_bam)])

        # Index new bam file: samtools index input.bam
        subprocess.call(['samtools', 'index', 'results/lumpy/{}_rg.bam'.format(filename)])

        start_time = time.perf_counter()

        # Run lumpy: lumpyexpress -B my.bam -o output.vcf
        proc = subprocess.Popen(['lumpyexpress', '-B', 'results/lumpy/{}_rg.bam'.format(filename), '-o', 'lumpy_acc.vcf'])

        # Get peak memory for lumpyexpress process
        process = psutil.Process(proc.pid)
        peak_memory = 0

        while proc.poll() is None:
            memory = process.memory_info().rss
            if memory > peak_memory:
                    peak_memory = memory
            time.sleep(0.1)
    
        # time complexity lumpy
        end_time = time.perf_counter()

        write_header = (
            not os.path.exists('lumpy_complexity.csv') or os.path.getsize('lumpy_complexity.csv') == 0)

        with open('lumpy_complexity.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow([
                    "input", "runtime_seconds", "peak_memory_mb"
                ])
            writer.writerow([
                input_bam, round(end_time - start_time, 3), peak_memory / (1024.0 ** 2) # convert to MB
            ])