#!/bin/bash
#SBATCH -p sched_mit_g4nier
#SBATCH -N 1
#SBATCH --mem 8G
#SBATCH -J PULpy-bacteroidetes-MAGs
#SBATCH -o PULpy-bacteroidetes-MAGs.out
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=ecutts@mit.edu

cd /home/ecutts/PULpy/
module add engaging/anaconda/2018.12

source activate snakemake
snakemake --use-conda --cores all
