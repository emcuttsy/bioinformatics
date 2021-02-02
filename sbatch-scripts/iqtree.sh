#!/bin/bash
#SBATCH -p sched_mit_g4nier
#SBATCH -N 1
#SBATCH -J iqtree_rprot-aln-all
#SBATCH -o iqtree_rprot-aln-all.out
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=ecutts@mit.edu

module add engaging/iqtree/1.6.3

cd ~/Bacteroidetes/rprot-concatenations/rprot-aln-all/
iqtree -s concatenated_alignment.aln -q partitions.txt -st AA -nt AUTO -bb 1000 -bnni
