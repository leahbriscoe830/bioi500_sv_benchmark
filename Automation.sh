#!/bin/bash

#The purpose of this script will be to automate testing of tools and pipe results into future testing
# Example:chmod +x run_batch.sh

# Hard-coded script paths
DELLY_SCRIPT="WIP_Delly_complexity.py"
TIDDIT_SCRIPT="WIP_TIDDIT_complexity.py"
MANTA_SCRIPT="WIP_manta_complexity.py"
LUMPY_SCRIPT="WIP_lumpy_complexity.py"

# Conda environments
DELLY_ENV="delly_env"
TIDDIT_ENV="tiddit_env"
MANTA_ENV="manta_env"
LUMPY_ENV="lumpy_env"

# Shared benchmark CSV
BENCHMARK_CSV="benchmark.csv"


# Parse arguments
while getopts "i:r:" opt; do
    case $opt in
        i) INPUT_DIR="$OPTARG" ;;
        r) REFERENCE="$OPTARG" ;;
        *) echo "Usage: bash run_batch.sh -i input_directory -r reference.fasta"
           exit 1 ;;
    esac
done


# Check arguments
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "ERROR: Input directory not found"
    exit 1
fi

if [[ ! -f "$REFERENCE" ]]; then
    echo "ERROR: Reference file not found"
    exit 1
fi


# Initialize Conda for this shell
source "$(conda info --base)/etc/profile.d/conda.sh"


# Find BAM files recursively
mapfile -t BAM_FILES < <(find "$INPUT_DIR" -type f -name "*.bam" | sort)


# Run tools on every BAM
for BAM in "${BAM_FILES[@]}"; do

    # Delly
    echo "Running Delly..."
    conda activate "$DELLY_ENV"

    python "$DELLY_SCRIPT" \
        -i "$BAM" \
        -o "$BENCHMARK_CSV" \
        -r "$REFERENCE"

    conda deactivate


    # TIDDIT
    echo "Running TIDDIT..."
    conda activate "$TIDDIT_ENV"

    python "$TIDDIT_SCRIPT" \
        -i "$BAM" \
        -o "$BENCHMARK_CSV" \
        -r "$REFERENCE"

    conda deactivate


    # Manta
    echo "Running Manta..."
    conda activate "$MANTA_ENV"

    python "$MANTA_SCRIPT" \
        -i "$BAM" \
        -o "$BENCHMARK_CSV" \
        -r "$REFERENCE"

    conda deactivate


    # Lumpy
    echo "Running Lumpy..."
    conda activate "$LUMPY_ENV"

    python "$LUMPY_SCRIPT" \
        -i "$BAM" \
        -o "$BENCHMARK_CSV" \
        -r "$REFERENCE"

    conda deactivate

done


