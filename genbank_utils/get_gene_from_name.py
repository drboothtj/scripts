'''
extract a protein sequence from a genbank file by name
HINT: it is wise to check with grep first
  arguments:
    [1]: path to genbank file
    [2]: name to extract (case sensetive)
'''

from Bio import SeqIO
from sys import argv
from typing import Tuple, List
from os import path

def write_fasta(gene:Tuple[str,str], outfile_name: str) -> None:
  with open(outfile_name, "w") as outfile:
      outfile.write('>' + gene[0]+ '\n')
      outfile.write(gene[1] + '\n')
 

def extract_genes(filename:str, name:str) -> List[Tuple[str, str]]:
  genes = []
  for record in SeqIO.parse(filename, "genbank"):
    for feature in record.features:
      if feature.type == "CDS":
        if 'gene' in feature.qualifiers:
            gene_name = feature.qualifiers['gene'][0]
            if name == gene_name:
              sequence = feature.qualifiers['translation'][0]
              gene = (name,sequence)
              genes.append(gene)
  return genes


def main(genbank:str, name:str) -> None:
  print(f'Extracting {name} from {genbank}!')
  genes = extract_genes(genbank, name)
  outfile_name = path.splitext(genbank)[0] + '_' + name + '.faa'
  for gene in genes:
    write_fasta(gene, outfile_name)

genbank = argv[1]
name = argv[2]
main(genbank, name)


