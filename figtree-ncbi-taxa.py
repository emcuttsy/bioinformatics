#!/usr/anaconda3/bin/python
#!/usr/bin/env python3
"""
Created on Mon Oct 22 23:50:11 2018

@author: Elise Cutts based on Erik Tamre and Thiberio Rangel

"""

import ete3, sys, argparse
from Bio import Entrez

# Parse arguments
parser=argparse.ArgumentParser(
    description='''Takes a Newick tree with leaf names of either NCBI taxids or
     sequence accesssions and returns a NEXUS tree with taxonomy information
     that can be read by FigTree. EDIT SCRIPT WITH YOUR ENTREZ EMAIL & API KEY FIRST ''',
     usage = '%(prog)s [-h] [-i input] [-o output] [-db NCBI database (i.e. protein)] [--taxid include if your tree leaves are NCBI taxids instead of sequence accessions]',
     epilog = '''Note: this script will create a local copy of the NCBI taxonomy
     database if one does not already exist. See the documentation for
     ete3.NCBITaxa() for more information.'''
     )
parser.add_argument('-i','--input', help='Tree file in Newick format', metavar='')
parser.add_argument('-o','--output', help='Name of output file. Default: <input>.figTree', metavar='')
parser.add_argument('-db', '--database', help='NCBI database for sequences', default='protein')
parser.add_argument('--taxid', help='Pass --taxid if your tree leaves are NCBI taxids instead of accessions', metavar='', nargs='?', const=True, default=False)

args = parser.parse_args()

# !!!!!!!!!!!!!!!!!!!
# Entrez API - EDIT THIS WITH YOUR INFORMATION BEFORE RUNNING
Entrez.email = 'ecutts@mit.edu' # REPLACE WITH YOUR EMAIL
Entrez.api_key = '057f36326473f362b4123bee57854f2c3208' # REPLACE WITH YOUR API KEY
database = str(args.database)
# !!!!!!!!!!!!!!!!!!!!

# Throw errors if the user did not provide an input
if args.input is None:
    raise ValueError('No input tree was provided')

# Get input and output paths
input = str(args.input)
if args.output is None:
    output = input + '.figTree'
else:
    output = str(args.output)

# Prepare taxonomy from ete3. Creates local copy of taxonomy db the first time it is used
ncbi = ete3.NCBITaxa()
ranks = ['class', 'phylum', 'order', 'family', 'genus', 'superkingdom', 'kingdom'] # ranks to include in the FigTree annotation

# Open the input nexus tree and write the first lines of the output tree file
tree = ete3.Tree(input, format=1) #format 1 = tree
out = open(output, 'w')
out.write("#NEXUS\nbegin taxa;\n\tdimensions ntax=%i;\n\ttaxlabels\n" %len(tree))

taxa2search = [] # counterintuitively this is actually a list of protein/sequence accessions to search
counter = 0 # tracks the current node of the tree
organism_list = [] # list of organism names associated with taxa2search accessions

# Add all sequence accessions on your tree to the list taxa2search
# taxa2search is counterintuitively the protein
for node in tree.get_leaves():
        taxon_name = node.name

#        My tree leaf names were not 'clean' protein accessions, so I used the code below to parse node names
#        If your leaf names are 'clean' NCBI protein/DNA accessions, you don't need anything like this
#
#        if not taxon_name.startswith('MAG'):
#            taxon_name = taxon_name.split('_')[0]

        taxa2search.append(str(taxon_name))

# Function that writes the comments containing taxonomy information for a node
def write_taxids(taxid, organism):
    lineage = {j:i for i,j in ncbi.get_rank(ncbi.get_lineage(taxid)).items()}
    # get a dictionary of the lineage of the organism based on taxid using ete3.get_rank and ete3.get_lineage
    # returns a dictionary of taxids with keys as the taxonomy levels
    lineage_names = ncbi.get_taxid_translator(lineage.values()) # translate lineage taxids to names

    print(lineage) # I like printing these just to see what's going on. Comment out if you like

    out.write('\t%s' %(node.name)) # write the name of the node
    comment = []
    comment.append('tax_organism="%s"' %organism) # add the organism name to the 'organism' taxonomy level
    for rank in ranks: # for taxonomic rank in the ranks list
        if rank in lineage: # for every rank in the lineage dictionary for this organism
            comment.append('tax_%s="%s"' % (rank, lineage_names[lineage[rank]])) # append the taxonomic group at that rank
    out.write('[&%s]\n' %' '.join(comment)) # write the comment into the output file
    return

# Function I wrote to write the name of non-NCBI sequences in all the taxonomy fields
# Without it you won't see the name of the sequence when you view taxonomy in FigTree
def write_name(name):
    out.write('\t%s' %(node.name))
    comment = []
    comment.append('tax_organism="%s"' %name)
    for rank in ranks:
        comment.append('tax_%s="%s"' % (rank, name))
    out.write('[&%s]\n' %' '.join(comment))
    return


# if tree leaves are sequence accessions, taxid needs to be found for each node
if args.taxid is False:
    records = [] # list containing NCBI records associated with sequence accessions in taxa2search
    for taxon in taxa2search: # for accession in taxa2search
        # attempt NCBI Entrez search of accession
        try:
            # if successful, append resulting record to records
            handle = Entrez.efetch(db='protein', id=taxon, retmode='xml')
            record = Entrez.read(handle)
            records.append(record)
        except:
            # if not successful, add dummy text
            records.append('not-taxid')
            print(taxon)

    for node in tree.get_leaves(): # for leaf in tree
        try:
            # get organism name
            # to understand the indexing, print a few of the records and look at them
            organism = records[counter][0]['GBSeq_organism']
            # get the taxid using ete3.ncbi.get_name_translator
            # organism is in a list because the function demands a list as input and doesn't work unless it gets a list
            # ¯\_(ツ)_/¯
            taxid = ncbi.get_name_translator([organism])
            # convert the dictionary output of ete3.get_name_translator into a simple string
            taxid = list(taxid.values())[0][0]
        except:
            # if you can't get an organism and/or taxid, don't return a taxid
            taxid = None
        counter += 1 #step one node forward

        if not taxid: # if there isn't a taxid
            write_name(node.name) # write the leaf name in every taxonomic category

            # alternatively, uncomment the lines below to simply write the name of the organism in the "name" and "organism" fields
            # out.write('\t%s\n' %(node.name))
            # comment = []
            # comment.append('tax_organism="%s"' % node.name)
            # out.write('[&%s]\n' %' '.join(comment))

        else: # if there IS a taxid
            write_taxids(taxid, organism) # write the taxonomy in comments in the output file
            # see above for function comments

# if tree leaves are already taxids, skip straight to writing lineage
# I added this myself since I sometimes make trees with taxid leaf names
else:
    for node in tree.get_leaves():
        taxid = node.name # taxid is simply the node name

#        My tree leaf names were not 'clean' protein accessions, so I used the code below to parse node names
#        If your leaf names are 'clean' NCBI protein/DNA accessions, you don't need anything like this
#
#        if not taxid.startswith('MAG'):
#            taxid = taxid.split('_')[0]
        try:
            organism = ncbi.get_taxid_translator([taxid])[int(taxid)]
            write_taxids(taxid, organism)
            print(organism) # Remove if you like.
        except:
            write_name(node.name)


newick_text = tree.write(format=1) # write the output tree
out.write(';\nend;\n') # add some final formatting to the output tree necessary for nexus format
out.write('begin trees;\n\ttree tree_1 = [&R] %s\nend;' %newick_text) # nexus formatting
out.close() # close the output file
