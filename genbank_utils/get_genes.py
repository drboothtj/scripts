'''
get the region surrounding a CDS 'gene'
  argv[1]: filename
  argv [2:] : list of gene names
'''
from Bio import SeqIO
from sys import argv
from typing import List
import os


def extract_genes(filename, genes):
  '''
  search genbank file for CDS features with specific values in the gene qualifier
    arguments:
      filename: path to genbank file
      genes: gene names to search for
    returns:
      gene_features: list of gene features that were hit 
  '''
  fasta_text = []
  for record in SeqIO.parse(filename, "genbank"):
    for feature in record.features:
      if feature.type == "CDS":
        if 'gene' in feature.qualifiers and feature.qualifiers['gene'][0] in genes:
            name = feature.qualifiers['gene'][0],
            start = int(feature.location.start)
            stop = int(feature.location.end)
            # in case gene is reversed
            left_boundary = min(start,stop) - 500
            right_boundary = max(start,stop) + 500
            seq = record.seq[left_boundary:right_boundary]
            fasta_text.append('>' + str(record.id) + '_'+ str(name) + '\n')
            fasta_text.append(str(seq) + '\n')
  return fasta_text

def write_file(filename, fasta_text):
  '''
  '''
  print('Writing to: ' + filename)
  with open(filename, 'w') as file:
    for line in fasta_text:
      file.write(line)

def main(filename: str, genes: List):
  '''
  main routine
    arguments: 
      filename: path to genbank file
      genes: gene names to search for
  '''
  print(f'looking for {genes} in {filename}')
  fasta_filename = os.path.splitext(filename)[0] + '.fasta'
  fasta_text = extract_genes(filename, genes)
  write_file(fasta_filename, fasta_text)



filename = argv[1]
genes = argv[2:]
main (filename, genes)
