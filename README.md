# Structural Variant Caller Benchmarking Project
Project for BIOI500 Advanced Bioinformatics benchmarking structural variant callers

#Overview
In this project, we will benchmark four different Structural Variant tools on memory usage and runtime. When looking at all the tools, we first need to establish a baseline of operation. For inputs, we are ideally looking at human paired-end sequencing, preferably BAM files. However, after that shared similarity of inputs, the way these programs build alignment and identify SV’s is diverse. The tools we are choosing to test are Delly, Lumpy, Manta, and TIDDIT. For the testing dataset, we chose to go with NIST's Genome in a Bottle.

## Installation Instructions
To run the benchmarking pipeline, clone the repo and move into the directory throught the terminal:
```
git clone https://github.com/leahbriscoe830/bioi500_sv_benchmark.git
cd bioi500_sv_benchmark
```
To test the tools, you will need to install miniconda and create the conda environments found in the envs folder (do these steps only once):
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/miniconda3/bin/activate
```
For each .yaml file in envs:
```
conda env create -f conda_{}_env.yaml
```
Before running each tool, activate the desired environment (e.g. delly_env, lumpy_env, etc...):

```
conda activate {}_env
```

Once wrapper files are finished, we will include code examples of how to run them from the terminal. We will then also show example graphs that will be generated.

## Tool Instructions

Before running any of the tool scripts, downsample your input .bam file using the Data_splitting_Script.py. Example data for this project comes from [NIST's Genome in a Bottle](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/NIST_Stanford_Illumina_6kb_matepair/bams/GRCh38/).

### Delly
Currently, Delly has run with test data; experimenting with a Python wrapper to run the tool on the desired dataset and output results to a csv. The wrapper will use argparse to prompt the user to input the folder where data is stored, grabbing every bam file and the fa file in the folder. Afterwards, it will output the results into a csv in a newly generated results folder (if one does not exist already). This records the run time for each dataset in seconds and memory usage (MB).

### TIDDIT
Currently, TIDDIT has run with test data; experimenting with a Python wrapper to run the tool on the desired dataset and output results to a csv. The wrapper will use argparse to prompt the user to input the folder where data is stored, grabbing every bam file and the fa file in the folder. Afterwards, it will output the results into a csv in a newly generated results folder (if one does not exist already). This records the run time for each dataset in seconds and memory usage (MB).

### Lumpy
To test lumpy for time and memory complexity, activate the lumpy_env conda environment and run the lumpy_complexity.py script. When prompted for input, enter the path for your downsampled input files [not implemented yet]. The script will output a file lumpy_complexity.txt, with each row having the time (sec) and memory (MB) usage of lumpy for each subsample of the input file.

### Manta
To test manta for time and memory complexity, activate the manta_env conda environment and run the manta_complexity.py script. When prompted for input, enter the path for your downsampled input files [not implemented yet]. The script will output a file manta_complexity.txt, with each row having the time (sec) and memory (MB) usage of manta for each subsample of the input file.

## Tool References

Delly: https://github.com/dellytools/delly

TIDDIT: https://github.com/SciLifeLab/TIDDIT

Lumpy: https://github.com/arq5x/lumpy-sv

Manta: https://github.com/Illumina/manta
