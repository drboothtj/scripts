'''
spits out the GC content of all sequences in a fasta file

arguments:
    argv[1]: path to the .fasta file
'''
from sys import argv
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction as GC

filename = argv[1]

gc_contents = []
with open(filename) as f:
    for record in SeqIO.parse(f, 'fasta'):
        print(record.id)
        gc = GC(record)
        gc_contents.append(gc)
        print(gc)

print('minimum gc is ' , min(gc_contents))

