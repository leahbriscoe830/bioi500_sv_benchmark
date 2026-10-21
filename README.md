# Structural Variant Caller Benchmarking Project
Project for BIOI500 Advanced Bioinformatics benchmarking structural variant callers

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

## Tool Instructions

Before running any of the tool scripts, downsample your input .bam file using the Data_splitting_Script.py.

### Delly

### TIDDIT

### Lumpy
To test lumpy, activate the lumpy_env conda environment and run the lumpy_complexity.py script. When prompted for input, enter the path for your downsampled input files [not implemented yet].

### Manta
To test manta, activate the manta_env conda environment and run the manta_complexity.py script. When prompted for input, enter the path for your downsampled input files [not implemented yet].
