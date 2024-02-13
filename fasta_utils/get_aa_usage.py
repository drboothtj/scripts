'''
a script to count the usage of each amino acid from an .faa
    argv[1]: path to .faa
'''

from sys import argv
from Bio import SeqIO
from collections import Counter

def print_totals(counter):
    print('---')
    print('Total Amino Acid Frequency')
    print('---')                       
    for item in counter:
        print(f'{item[0]}: {item[1]}')
    print('---')     

def print_percentage(counter):
    total = sum([item[1] for item in counter])
    print('---')
    print('Percentage Amino Acid Frequency')
    print('---')                       
    for item in counter:
        percentage = (item[1]/total)*100
        print(f'{item[0]}: {percentage}')
    print('---')     

filename = argv[1]
total_sequence = ""

for record in SeqIO.parse(filename, "fasta"):
    total_sequence = total_sequence + record.seq

counter = Counter(total_sequence)
counter = sorted(counter.items())

print_totals(counter)
print_percentage(counter)
