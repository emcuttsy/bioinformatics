#!/bin/bash
#SBATCH -p sched_mit_g4nier
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=10G
#SBATCH --time=3-00:00:00
#SBATCH -J build_db
#SBATCH --output=dbbuild_%a.out
#SBATCH --error=dbbuild__%a.err
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=ecutts@mit.edu
#SBATCH --array=1-297

FILENAME=$(awk "NR==$SLURM_ARRAY_TASK_ID" genome-list.txt)

module add engaging/ncbi-blast/2.6.0+
makeblastdb -in $FILENAME -parse_seqids -dbtype prot -out $FILENAME
