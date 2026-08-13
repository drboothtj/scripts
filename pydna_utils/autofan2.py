'''
a script to automate the design of selfligation PCR for telomere characterisation in Streptomyces
version 2 uses primer3 for improved primer design

if you find this script helpful, please cite:
        Faurdal D et al., Tying up loose ends: Recovering thousands of missing telomeres from Streptomyces and other Streptomycetaceae genomes. BioRxiv, 2025

for the origional protcol see:
        Fan Y et al., A self-ligation method for PCR-sequencing the telomeres of Streptomyces and Mycobacterium linear replicons. J Microbiol Methods. 2012
        and;
        Algora-Gallardo L et al., Bilateral symmetry of linear streptomycete chromosomes. Microb Genom. 2021
        for origional method.

Written by T.J.B.
'''

from sys import argv
from Bio import Seq, SeqIO
from Bio.Restriction import RestrictionBatch

import primer3 as p3

def print_primer_line(seq, tm, name):
        '''
        print the primer details to the console
        NOTE:REVERSED FOR INVERSE PCR
        '''
        primer_line = [
                name,
                seq,
                str(len(seq)),
                str(tm)
                ]
        print(",".join(primer_line))

def design_primers(template, name: str):
        '''
        design primers for inverse PCR using pydna
                arguments:
                        template: a biopython seq record
                        name: a string identifier to name the primers
        '''
        template = str(template)
        centroid = len(template)//2
        rotated_template = template[centroid:] + template[:centroid]
        try:
                results = p3.bindings.design_primers(
                seq_args={
                    "SEQUENCE_TEMPLATE": rotated_template
                },
                global_args={
                        #"PRIMER_PICK_LEFT_PRIMER": 0,
                        "PRIMER_OPT_SIZE": 20,
                        "PRIMER_MIN_SIZE": 12,
                        "PRIMER_MAX_SIZE": 25,
                        "PRIMER_OPT_TM": 58.0,
                        "PRIMER_MIN_TM": 50.0,
                        "PRIMER_MAX_TM": 70.0,
                        "PRIMER_MAX_POLY_X": 3,
                        "PRIMER_NUM_RETURN": 10,
                        "PRIMER_PRODUCT_OPT_SIZE": 200,
                        "PRIMER_PRODUCT_SIZE_RANGE": [[centroid, 2000]]
                        },
                )
                print_primer_line(results["PRIMER_LEFT_0_SEQUENCE"], results["PRIMER_LEFT_0_TM"], name + "F")
                print_primer_line(results["PRIMER_RIGHT_0_SEQUENCE"], results["PRIMER_RIGHT_0_TM"], name + "R")
        except  OSError:
                print(f"No good primers found for {name}")
                
def digest(record):
        '''
        simulate digestion with blunt cutters
        '''
        cutters = RestrictionBatch(["SmaI", "PvuII"])
        cuts = cutters.search(record.seq)
        cut_positions = sorted([pos for positions in cuts.values() for pos in positions]) #to extract from dict
        left_fragment = record.seq[0:cut_positions[0]]
        right_fragment = record.seq[cut_positions[-1]:-1]
        return left_fragment, right_fragment

def main(genome_path: str) -> None:
        '''
        main routine for autofan.py
                arguments: 
                        genome_path: path to genome as string
                returns:
                        None
        '''
        records = SeqIO.parse(genome_path, "genbank")
        counter = 0
        for record in records:
                record_name = genome_path.split(".")[0] + '_' + str(counter)
                left_fragment, right_fragment = digest(record)
                design_primers(
                        left_fragment, record_name + "_left"
                )
                design_primers(
                        right_fragment, record_name + "_right"
                )
                counter +=1
       
GENOME_PATH = argv[1]
main(GENOME_PATH)

