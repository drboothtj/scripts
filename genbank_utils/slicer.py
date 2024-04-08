'''
create new .gbk from coordinates
    argv[1]: path to origional
    argv[2]: start location
    argv[3]: stop location
'''
from sys import argv
from Bio import SeqIO

def extract_region(genbank_file, start, end, output_file):
   # Parse the GenBank file
    record = SeqIO.read(genbank_file, "genbank")
    sub_record = record[start:end]
    SeqIO.write(sub_record, output_file, "genbank")

genbank_file = argv[1]
start = int(argv[2])
end = int(argv[3])
output_file = genbank_file.split('.')[0] + '_' + str(start) + '_' + str(end) + '.gbk'
extract_region(genbank_file, start, end, output_file)