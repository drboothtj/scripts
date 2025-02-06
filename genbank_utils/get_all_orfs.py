from Bio import SeqIO
from sys import argv
import os

def get_hits_by_tag(genbank_file, target_tag):
  lines_to_write = []
  for record in SeqIO.parse(genbank_file, "genbank"):
    for feature in record.features:
        if feature.type == "CDS":
            tags = feature.qualifiers.keys()
            if target_tag in tags:
                cds_name = feature.qualifiers.get(target_tag)
                cds_sequence = feature.extract(record.seq)
                lines_to_write.append('>' + str(cds_name[0]) + '\n')
                lines_to_write.append(str(cds_sequence)+ '\n')
  return(lines_to_write)

def write_lines(lines, filename):
  filename = os.path.splitext(filename)[0]
  filename += '.fna'
  with open(filename, "w") as f:
        for line in lines:
          f.writelines(line)

def main(genbank_file, target_tag):
  lines = get_hits_by_tag(genbank_file, target_tag)
  write_lines(lines, genbank_file)

genbank_file = argv[1]
target_tag = argv[2]
main(genbank_file, target_tag)

