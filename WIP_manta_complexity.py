import subprocess
import time
import os
import sys
import psutil
import argparse
import csv

# Example command: python WIP_manta_complexity.py -i subsamples/ -r /home/brendonleah/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna -c /home/user/miniconda3/envs/manta_env/bin/configManta.py
# Function to parse command-line arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(
        description="Run manta and record runtime and peak memory in a csv."
    )
    parser.add_argument(
        "-i", "--input",
        help="Directory where input BAM/CRAM subsampled files are located",
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
input_dir = arguments.input
ref_fa = arguments.reference # 'data/GCA_000001405.15_GRCh38_no_alt_plus_hs38d1_analysis_set.fna'
path_to_config = arguments.config_path # '/home/user/miniconda3/envs/manta_env/bin/configManta.py'

for input_bam in os.listdir(input_dir):
    if input_bam.startswith('HG002.GRCh38.300x_chr20_') and input_bam.endswith('pct.bam'):

        # Get full name for each file (minus extension)
        filename = os.path.splitext(os.path.basename('{}{}'.format(input_dir, input_bam)))[0]
        # Get subsample fraction
        frac = filename.split('_') # HG002.GRCh38.300x, chr20, 25pct

        # Configure manta: /path/to/manta/bin/configManta.py --bam=input.bam --referenceFasta=reference.fa --runDir=/path/to/manta_somatic_output
        subprocess.call([path_to_config, '--bam', '{}{}'.format(input_dir, input_bam), '--referenceFasta', ref_fa, '--runDir', 'results/manta/{}/'.format(filename)])

        start_time = time.time()
        
        # Run manta: python /path/to/manta_somatic_output/runWorkflow.py -m local -j 8
        proc = subprocess.Popen(['python', 'results/manta/{}/runWorkflow.py'.format(filename), '-m', 'local']) 

        # Get peak memory for manta workflow process
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

        # time complexity manta
        end_time = time.time()

        # Copy vcf into test_vcf directory, rename to appropriate frac name
        subprocess.call(['cp', 'results/manta/{}/results/variants/diploidSV.vcf.gz'.format(filename), 'test_vcfs/'])
        subprocess.call(['cp', 'results/manta/{}/results/variants/diploidSV.vcf.gz.tbi'.format(filename), 'test_vcfs/'])

        subprocess.call(['mv', 'test_vcfs/diploidSV.vcf.gz', 'manta_{}.vcf.gz'.format(frac[2])])
        subprocess.call(['mv', 'test_vcfs/diploidSV.vcf.gz.tbi', 'manta_{}.vcf.gz.tbi'.format(frac[2])])

        write_header = (
            not os.path.exists('manta_complexity.csv') or os.path.getsize('manta_complexity.csv') == 0)

        with open('manta_complexity.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow([
                    "tool", "input", "runtime_seconds", "peak_memory_mb"
                ])
            writer.writerow([
                'manta', input_bam, round(end_time - start_time, 3), peak_memory / (1024.0 ** 2)
            ])