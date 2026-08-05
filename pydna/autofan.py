'''
a script to automate the design of selfligation PCR for telomere characterisation in Streptomyces

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
from Bio import SeqIO
from Bio.Restriction import RestrictionBatch
from pydna.dseqrecord import Dseqrecord
from pydna.design import primer_design
from pydna.tm import tm_default

def print_primer_line(primer, name):
        '''
        print the primer details to the console
        NOTE:REVERSED FOR INVERSE PCR
        '''
        primer_line = [
                name,
                primer.seq.reverse_complement().__str__(),
                str(len(primer.seq)),
                str(tm_default(primer.seq))
                ]
        print(",".join(primer_line))

def design_primers(template, name: str):
        '''
        design primers for inverse PCR using pydna
                arguments:
                        template: a biopython seq record
                        name: a string identifier to name the primers
        '''
        template = Dseqrecord(template) #convert to pydna
        template.looped() #ensure circular
        centroid = len(template)//2
        amplicon = primer_design(template[centroid - 50: centroid + 50], target_tm=60) 
        print_primer_line(amplicon.forward_primer, name + "_R") #flipped for inverse PCR
        print_primer_line(amplicon.reverse_primer, name + "_F") #flipped for inverse PCR

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

