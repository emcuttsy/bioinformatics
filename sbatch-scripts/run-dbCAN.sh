#!/bin/bash
#SBATCH -p sched_mit_g4nier
#SBATCH -N 1
#SBATCH --mem=16G
#SBATCH -J run_dbcan
#SBATCH --output=run_dbcan_%a.out
#SBATCH --error=run_dbcan_%a.err
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=ecutts@mit.edu
#SBATCH --array=1-84

cd ~/dbCAN
PROTS=$(awk "NR==$SLURM_ARRAY_TASK_ID" inputs/input-proteins.txt)
GFF=$(awk "NR==$SLURM_ARRAY_TASK_ID" inputs/input-gffs.txt)

conda activate py39
python run_dbcan/run_dbcan.py --out_dir output $PROTS -c $GFF protein
