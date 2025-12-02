'''
convert gffs to gbks WITHOUT SEQUENCE
requires bcbio-gff in addition to biopython
  arguments:
    argv[1]: gff path
    argv[2]: output path (Can leave blank)
 '''
from sys import argv

from BCBio import GFF
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

def main(gff_file, out_gbk):
   # Parse GFF into a structure (BCBio handles hierarchy)
    gff_iter = GFF.parse(gff_file)
    gb_records = []
    for rec in gff_iter:
        rec.seq = Seq("")
        rec.annotations["molecule_type"] = "DNA"
        gb_records.append(rec)
    SeqIO.write(gb_records, out_gbk, "genbank")

INPUT = argv[1]
try:
  OUTPUT = argv[2]
except IndexError:
  OUTPUT = 'output.csv'

main(INPUT, OUTPUT)

