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
     that can be read by FigTree.''',
     usage = '%(prog)s [-h] [-i input] [-o output] [-e entrez email]',
     epilog = '''Note: this script will create a local copy of the NCBI taxonomy
     database if one does not already exist. See the documentation for
     ete3.NCBITaxa() for more information.'''
     )
parser.add_argument('-i','--input', help='Tree file in Newick format', metavar='')
parser.add_argument('-o','--output', help='Name of output file. Default: <input>.figTree', metavar='')
parser.add_argument('-ee','--entrez-email', help='Entrez email.', metavar='')
parser.add_argument('--api-key', help='Entrez API key')
parser.add_argument('-db', '--database', help='NCBI database for sequences', default='protein')
parser.add_argument('--taxid', help='Pass --taxid if your tree leaves are NCBI taxids instead of accessions', metavar='', nargs='?', const=True, default=False)

args = parser.parse_args()

# Entrez API
Entrez.email = args.entrez_email
Entrez.email = 'ecutts@mit.edu' # delete or replace with yours
Entrez.api_key = args.api_key
Entrez.api_key = '057f36326473f362b4123bee57854f2c3208' # delete or replace with yours
database = str(args.database)

# Throw errors if the user did not provide an input and Entrez email
if Entrez.email is None:
    raise ValueError('No Entrez email was provided')
if args.input is None:
    raise ValueError('No input tree was provided')

# Input and output
input = str(args.input)
if args.output is None:
    output = input + '.figTree'
else:
    output = str(args.output)

ncbi = ete3.NCBITaxa() #load NCBI taxa from ete3
ranks = ['class', 'phylum', 'order', 'family', 'genus', 'superkingdom', 'kingdom']
tree = ete3.Tree(input, format=1)
out = open(output, 'w')
out.write("#NEXUS\nbegin taxa;\n\tdimensions ntax=%i;\n\ttaxlabels\n" %len(tree))

taxa2search = []
counter = 0
organism_list = []

for node in tree.get_leaves():
        taxon_name = node.name
        if not taxon_name.startswith('MAG'): #THIS IS MY OWN CODE FOR MY OWN STUFF. COMMENT OUT?
            taxon_name = taxon_name.split('_')[0]
        taxa2search.append(str(taxon_name))

def write_taxids(taxid, organism):
    lineage = {j:i for i,j in ncbi.get_rank(ncbi.get_lineage(taxid)).items()}
    print(lineage)
    lineage_names = ncbi.get_taxid_translator(lineage.values())
    out.write('\t%s' %(node.name))
    comment = []
    comment.append('tax_organism="%s"' %organism)
    for rank in ranks:
        if rank in lineage:
            comment.append('tax_%s="%s"' % (rank, lineage_names[lineage[rank]]))
    out.write('[&%s]\n' %' '.join(comment))
    return

def write_MAGs(name):
    out.write('\t%s' %(node.name))
    comment = []
    comment.append('tax_organism="%s"' %name)
    for rank in ranks:
        comment.append('tax_%s="%s"' % (rank, 'MAG'))
    out.write('[&%s]\n' %' '.join(comment))
    return



if args.taxid is False: # if taxids are passed, this part is unnecessary
    records = []
    for taxon in taxa2search:
        try:
            handle = Entrez.efetch(db='protein', id=taxon, retmode='xml')
            record = Entrez.read(handle)
            records.append(record)
        except:
            records.append('not-taxid')
    for node in tree.get_leaves():
        try:
            organism = records[counter][0]['GBSeq_organism']
            taxid = ncbi.get_name_translator([organism])
            taxid = list(taxid.values())[0][0]
        except:
            taxid = None
        counter += 1
        if not taxid:
            out.write('\t%s\n' %(node.name))
            comment = []
            comment.append('tax_organism="%s"' % node.name)
            for rank in ranks:
                comment.append('tax_%s="%s"' % (rank,node.name))
            out.write('[&%s]\n' %' '.join(comment))
        else:
            write_taxids(taxid, organism)

else:
    for node in tree.get_leaves():
        taxid = node.name

        taxid = node.name
        if not taxid.startswith('MAG'): #THIS IS MY OWN CODE FOR MY OWN STUFF. COMMENT OUT?
            taxid = taxid.split('_')[0]
            organism = ncbi.get_taxid_translator([taxid])[int(taxid)]
            write_taxids(taxid, organism)
            print(organism)
        else:
            write_MAGs(taxid)


newick_text = tree.write(format=1)
out.write(';\nend;\n')
out.write('begin trees;\n\ttree tree_1 = [&R] %s\nend;' %newick_text)
out.close()
