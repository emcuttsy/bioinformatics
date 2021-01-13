#!/bin/bash
#SBATCH -p sched_mit_g4nier
#SBATCH -N 1
#SBATCH --mem 2G
#SBATCH -J PULpy-bacteroidetes-MAGs
#SBATCH -o PULpy-bacteroidetes-MAGs.out
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=ecutts@mit.edu

conda activate snakemake
cd ~/PULpy/
snakemake --use-conda --cores all
