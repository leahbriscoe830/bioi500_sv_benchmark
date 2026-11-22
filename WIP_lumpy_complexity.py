import subprocess
import time
import os
import sys
import psutil
import argparse
import csv

# Example command: python WIP_lumpy_complexity.py -i subsamples/ -r /home/brendonleah/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna
# Function to parse command-line arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="Run lumpy and record runtime and peak memory in a csv."
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
        help="Reference genome FASTA file.",
        required=True
    )
    return parser.parse_args(args)

# Retrieve command-line arguments
arguments = check_arg(sys.argv[1:])
infile = arguments.input
outfile = arguments.output
reference = arguments.reference # /home/brendonleah/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna


# Get full name for each file (minus extension)
filename = os.path.splitext(os.path.basename(infile))[0]
# Get subsample fraction
frac = filename.split('_') # HG002.GRCh38.300x, chr20, 25pct

if not os.path.isdir('results/lumpy/'):
    os.makedirs('results/lumpy/')

# Add dummy read group header: samtools addreplacerg -r '@RG\tID:sample1\tLB:lib1\tPL:ILLUMINA\tSM:sample1' -o output.bam input.bam
subprocess.call(['samtools', 'addreplacerg', '-r', '@RG\tID:sample1\tLB:lib1\tPL:ILLUMINA\tSM:sample1', '-o', 'results/lumpy/{}_rg.bam'.format(filename), infile])

# Index new bam file: samtools index input.bam
subprocess.call(['samtools', 'index', 'results/lumpy/{}_rg.bam'.format(filename)])

start_time = time.time()

# Run lumpy: lumpyexpress -B my.bam -o output.vcf
proc = subprocess.Popen(['lumpyexpress', '-B', 'results/lumpy/{}_rg.bam'.format(filename), '-o', 'test_vcfs/lumpy_{}_init.vcf'.format(frac[2])])

# Get peak memory for lumpyexpress process (and subprocesses)
root_process = psutil.Process(proc.pid)
peak_memory = 0

while proc.poll() is None:
    try:
        processes = [root_process]
        processes.extend(root_process.children(recursive=True))

        current_memory = 0

        for p in processes:
            try:
                current_memory += p.memory_info().rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        peak_memory = max(peak_memory, current_memory)

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    time.sleep(0.1)

# time complexity lumpy
end_time = time.time()

# Pre processing for truvari benchmark (WIP):
# grep '^#' input.vcf > header.vcf
with open('test_vcfs/lumpy_{}_sorted.vcf'.format(frac[2]), 'w') as out:
    subprocess.call(['grep', '^#', 'test_vcfs/lumpy_{}_init.vcf'.format(frac[2])], stdout=out)

#grep -v '^#' input.vcf | sort -k1,1 -k2,2n >> header.vcf
cmd = "grep -v '^#' test_vcfs/lumpy_{0}_init.vcf | sort -k1,1 -k2,2n >> test_vcfs/lumpy_{0}_sorted.vcf".format(frac[2])
subprocess.call(cmd, shell=True)

subprocess.call(['bgzip', 'test_vcfs/lumpy_{}_sorted.vcf'.format(frac[2])])

#tabix -p vcf sorted.vcf.gz
subprocess.call(['tabix', '-p', 'vcf', 'test_vcfs/lumpy_{}_sorted.vcf.gz'.format(frac[2])])

#bcftools reheader --fai reference.fa.fai input.vcf.gz -o fixed.vcf.gz
subprocess.call(['bcftools', 'reheader', '--fai', '{}.fai'.format(reference), 'test_vcfs/lumpy_{}_sorted.vcf.gz'.format(frac[2]), '-o', 'test_vcfs/lumpy_{}.vcf.gz'.format(frac[2])])
subprocess.call(['tabix', '-p', 'vcf', 'test_vcfs/lumpy_{}.vcf.gz'.format(frac[2])])

# Write to CSV
write_header = (
    not os.path.exists(outfile) or os.path.getsize(outfile) == 0)

with open(outfile, 'ab') as csvfile:
    writer = csv.writer(csvfile)

    if write_header:
        writer.writerow([
            "tool", "input",
            "runtime_seconds", "peak_memory_mb", "exit_code"
        ])
        
    writer.writerow([
        'lumpy', filename,
        round(end_time - start_time, 3), peak_memory / (1024.0 ** 2), 0 # exit code WIP
    ]) 