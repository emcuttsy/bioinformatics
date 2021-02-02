#!/bin/bash
#SBATCH -p sched_mit_g4nier
#SBATCH -N 1
#SBATCH --mem=16G
#SBATCH -J run_dbcan
#SBATCH --output=run_dbcan_%a.out
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=ecutts@mit.edu
#SBATCH --array=1-84

cd /home/ecutts/dbCAN/run_dbcan
module add engaging/anaconda/2018.12
while read p; do
	mkdir -p ../output/$p
done < ../input/magslist.txt

PROTS=$(awk "NR==$SLURM_ARRAY_TASK_ID" ../input/input-proteins.txt)
GFF=$(awk "NR==$SLURM_ARRAY_TASK_ID" ../input/input-gffs.txt)
NAMES=$(awk "NR==$SLURM_ARRAY_TASK_ID" ../input/magslist.txt)

source activate py39
python run_dbcan.py --out_dir ../output/$NAMES ../input/$PROTS -c ../input/$GFF protein
