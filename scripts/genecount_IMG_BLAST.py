#!/usr/bin/python3
import pandas as pd
import numpy as np
import string

# counts genes in results from an IMG Blast result
def count_gene_IMGblast(df, genes, name_col = 'Genome Name',\
skip_tails = ''):
    """A function that counts occurences of genes in each genome represented in a DataFrame of IMG/JGI BLAST results and returns a DataFrame with one row per genome. Not case-sensitive.

    Args:
        df (DataFrame): BLASTp results from IMG/JGI
        genes (list of str): genes to search for within 'Gene Name' column of df
        name_col (str): column of df to use as identification for each genome
            (default: 'Genome Name')
        skip_tails (str): allows occurences of the gene search terms that are
            followed by a number, letter, or either to be ignored. Used to prevent
            double-counting (i.e. 'L20' counting for 'L2'). Use 'alphanumeric',
            'numeric', or 'alpha' to avoid double counting instances when your
            search gene is followed by a letter or number, number, or letter,
            respectively. When set to '', no double-counts are excluded.
                (default: '')

    Returns:
        countdf (list): a list of strings representing the header columns
    """
    temp = dict.fromkeys(genes)
    for key in temp.keys():
        temp[key] = dict.fromkeys(set(df[name_col]), 0)

    for index, row in df.iterrows():
        for gene in genes:
            gene_w_tail = add_string_tails(gene, skip_tails)
            substringError = False
            for i in gene_w_tail:
                    if i in row['Gene Name'].lower():
                        print('Substring Error!')
            if gene.lower() in row['Gene Name'].lower() and not substringError:
                temp[gene][row[name_col]] += 1
    countdf = pd.DataFrame(temp) #easy to read format but bad for plotting
    countdf.reset_index(inplace=True)
    countdf.rename(columns={'index':'Shortname'}, inplace=True)
    return countdf

def add_string_tails(istring, tails_category):
    if tails_category == '':
        return istring

    elif tails_category == 'alphanumeric':
        tails = string.ascii_lowercase + string.digits
    elif tails_category == 'alpha':
        tails = string.ascii_lowercase
    elif tails_category == 'numeric':
        tails = string.digits

    return [istring.lower() + char for char in tails]
