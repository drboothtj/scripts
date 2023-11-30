'''get individual regions from .gbk '''
import sys
from typing import List
from Bio import SeqIO

def get_records_from_genbank(filename: str) -> List:
    records = []
    with open(filename, "r") as genbank_file:
        for record in SeqIO.parse(genbank_file, "genbank"):
            records.append(record)
    return records

def write_records(records: List) -> None:
    for record in records:
        filename = record.id + ".gbk"
        with open(filename, "w") as genbank_file:
            SeqIO.write(record, genbank_file, "genbank")

### main routine ###
filename = sys.argv[1]
records = get_records_from_genbank(filename)
write_records(records)

