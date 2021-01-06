#!/bin/bash
#SBATCH -p sched_mit_g4nier
#SBATCH -N 1
#SBATCH --mem=6G
#SBATCH -J iqtree_csulf_amidohydrolase_homologs
#SBATCH -o iqtree_csulf_amidohydrolase_homologs.out
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=ecutts@mit.edu

module add engaging/iqtree/1.6.3

cd ~/Amidohydrolases/tree-ncbi7001200-treesample/
iqtree -s amidohydrolase-plusTreeSample.aln -st AA -nt AUTO -mem 6G
