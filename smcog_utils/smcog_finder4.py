#!/usr/bin/env python3
'''
smcog_finder.py - a script for extracting loci with specific SMCOG numbers from antiSMASH outputs
usage:
    smcog_finder.py DIRECTORY SMCOG_NUMBER
functions:
    strip_duplicate_cds(record: SeqRecord) -> SeqRecord 
    run(directory: str, smcog_number: int)-> None
'''
import glob
import os
import sys
import antismash
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def strip_duplicate_cds(record: SeqRecord) -> SeqRecord:
    '''
    removes duplicate CDS annotations to avoid errors
        arguments:
            record: an antismash record
        returns:
            record: the record with duplicate CDSs removed
    '''
    locations = set()
    features = []
    for feature in record.features:
        if feature.type != "CDS":
            continue
        if str(feature.location) in locations:
            continue
        features.append(feature)
        locations.add(str(feature.location))
    record.features = features
    return record

def run(directory: str, smcog_number: int)-> None: 
    '''
    main routine for smcog_finder
        arguments:
            directory: path to directory containing antiSMASH results
            smcog_number: interger of the SMCOG to find
        returns:
            None
    '''
    for file in glob.glob(os.path.join(directory, "*.gbk")):
        print(file)
        cdses = []
        record = strip_duplicate_cds(list(SeqIO.parse(file, "genbank"))[0])
        record = antismash.common.secmet.Record.from_biopython(record, "bacteria")
        for cds in record.get_cds_features():
            for f in cds.gene_functions.get_by_tool("smcogs"):
                if f.product == "SMCOG%d" % smcog_number:
                    print(cds)
                    cdses.append(("%s|%s" % (record.id, cds.get_name()), cds))
                    break
        
        with open("SMCOG%d.fasta" % smcog_number, "a+") as handle:
            for name, cds in cdses:
                handle.write(">%s\n%s\n" % (name, cds.location.extract(record.seq)))
        with open("SMCOG%d.faa" % smcog_number, "a+") as handle:
            for name, cds in cdses:
                handle.write(">%s\n%s\n" % (name, cds.translation))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: %s gbk_dir smcog_number" % (sys.argv[0]))
        sys.exit(1)
    run(str(sys.argv[1]), int(sys.argv[2]))
