import subprocess
import os
import sys
import argparse

#function to parse command line arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(description="<add description of what script does>")
    parser.add_argument("-i", "--input",
    help="input file",
    required=True)
    return parser.parse_args(args)

#retrieve command line arguments
arguments = check_arg(sys.argv[1:])
infile = arguments.input

#Downsample BAM to desired fraction
def downsample_bam(input_bam, output_bam, fraction):
    cmd = [
        "samtools", "view",
        "-b",
        "-s", f"42.{int(fraction * 100):02d}",
        "-o", output_bam,
        input_bam
    ]

    result = subprocess.run(cmd,capture_output=True,text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        return

    print(f"Created {output_bam}")

# Example usage
input_bam = infile
fractions = [0.25, 0.50, 0.75, 1.0]

for frac in fractions:
    filename = os.path.basename(input_bam)
    output_bam = f"{os.path.splitext(filename)[0]}_{int(frac * 100)}pct.bam"
    downsample_bam(input_bam, output_bam, frac)


print("Downsampling complete.")