'''
Create a csv table of all recordnames, locus_tags and products from a .gbk file
    arguments:
        argv[1]:
            glob string for path to genbank files
'''
import csv
import glob

from sys import argv
from typing import List

from Bio import SeqIO



def write_lines(lines: List) -> None:
    '''
    write lines to a file
        arguments:
            lines: list of lines to write
        returns:
            None
    '''
    with open("out.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for line in lines:
            writer.writerow(line)

def get_lines(genbank_files: List) -> List:
    '''
    get annotations from the gbk files and return as a list of lines
        arguments:
            genbank_files: list of file paths
        returns:
            lines: list of lines containing annotations
    '''
    lines = []

    for gb_file in genbank_files:
        for record in SeqIO.parse(gb_file, "genbank"):
            record_name = record.name
            for feature in record.features:
                if feature.type == "CDS":
                    locus_tag = feature.qualifiers.get("locus_tag", [""])[0]
                    gene = feature.qualifiers.get("gene", [""])[0]
                    product = feature.qualifiers.get("product", [""])[0]
                    gene_function = feature.qualifiers.get("gene_functions", [""])[0]
                    lines.append([record_name, locus_tag, gene, product, gene_function])
    return lines


def main(genbank_files: List) -> None:
    '''
    main routine
        arguments:
            genbank_files: list of file paths
        returns:
            None
    '''
    lines = get_lines(genbank_files)
    write_lines(lines)

GBKS = glob.glob(argv[1])
main(GBKS)
