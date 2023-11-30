'''
converts CDSs in a genbank file to .faa format
	arguments:
		argv[1]: path to genbank file
'''

from Bio import SeqIO
from sys import argv
import os

in_file_name = argv[1]
out_file_name = os.path.splitext(in_file_name)[0] + '.faa'

all_cdses = []
with open(in_file_name, 'r') as GBFile:
    genbank_cdses = SeqIO.InsdcIO.GenBankCdsFeatureIterator(GBFile)

    for cds in genbank_cdses:
        if cds.seq is not None:
            cds.id = cds.name
            cds.description = ''
            all_cdses.append(cds)
SeqIO.write(all_cdses, out_file_name, 'fasta')
