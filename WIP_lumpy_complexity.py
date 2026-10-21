import subprocess
import time
import os
import psutil

subsamples = [0.01, 0.02, 0.03, 0.04, 0.05] # exact downsample fractions TBD
times = [] # measure time across 5 subsamples of input bam
mem_usage = [] # measure memory across 5 subsamples of input bam
input_bam = '/home/brendonleah/data/HG002.sorted.bam' # use argparse?

for frac in subsamples:
    # Downsample input bam file: samtools view -b -s 0.01 -o downsampled.bam input.bam
    subprocess.call(['samtools', 'view', '-b', '-s', str(frac), '-o', '{}_input.bam'.format(frac), input_bam])

    # Add dummy read group header: samtools addreplacerg -r '@RG\tID:sample1\tLB:lib1\tPL:ILLUMINA\tSM:sample1' -o output.bam input.bam
    subprocess.call(['samtools', 'addreplacerg', '-r', '@RG\tID:sample1\tLB:lib1\tPL:ILLUMINA\tSM:sample1', '-o', 'results/lumpy/{}_input_rg.bam'.format(frac), '{}_input.bam'.format(frac)])

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