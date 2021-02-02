#!/bin/bash
#SBATCH -p sched_mit_g4nier
#SBATCH -N 1
#SBATCH --mem 16G
#SBATCH -J PULpy-saprospiria
#SBATCH -o PULpy-saprospiria.out
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=ecutts@mit.edu

cd /home/ecutts/PULpy/
module add engaging/anaconda/2018.12

source activate snakemake
snakemake --use-conda --cores all
