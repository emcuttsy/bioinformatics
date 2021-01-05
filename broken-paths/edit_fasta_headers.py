# be sure to change the file paths appropriately.
# run in the directory containing the directories of genomes from ncbi-genome-download
import pandas as pd
taxonomy_info = pd.read_csv('../ANI_report_prokaryotes.csv')

from Bio import SeqIO
import os

def edit_fasta_headers(ifile, output_path='output/'):

    assembly = 'GCF_' + os.path.basename(ifile).split('_')[1]
    taxid = taxonomy_info[taxonomy_info['refseq-accession'] == assembly]['taxid'].tolist()[0]
    name = taxonomy_info[taxonomy_info['refseq-accession'] == assembly]['organism-name'].tolist()[0]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ofile = output_path + str(taxid) + "_" + name.replace(" ", "_") + ".faa"

    with open(ifile) as original, open(ofile, 'w') as corrected:
        records = SeqIO.parse(original, 'fasta')
        for record in records:
            description = record.description.split(record.id)[1].split('[')[0]
            record.description ='taxid' + str(taxid) + description + ' [' + name + ']'
            SeqIO.write(record, corrected, 'fasta')

current_directory = os.getcwd()
for directory in [x[0] for x in os.walk(current_directory)]:
    print(directory)
    for file in os.listdir(directory):
        if file.endswith(".faa"):
            edit_fasta_headers(directory +'/' + file, output_path = '../fastas/')
