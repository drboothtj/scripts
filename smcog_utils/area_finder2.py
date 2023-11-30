#!/usr/bin/env python3
'''
extracts areas associated with a specific SMCOG annotation from a direcroy of genbank files
	agruments:
		argv[1]: path to directory containing genbank files ".gbk"
		argv[2]: SMCOG number to search for
		argv[3]: path to an output directory for resulting genbank files
'''
import glob
import os
import sys

import antismash
from Bio import SeqIO

def strip_duplicate_cds(record):
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

def search_nbc(record_name, cds_name):
    file = record_name + '.gbk'
    records = antismash.common.secmet.Record.from_genbank(file, "bacteria")
    for record in records:
        if cds_name in record.get_cds_name_mapping():
            return record
    print('File found, protein not found.')
    return None

def get_region(cds_name, record, output_dir):
    try:
        cds = record.get_cds_by_name(cds_name)
        filename = os.path.join(output_dir, cds_name + ".gbk")
        print('Writing to ' + filename)
    except IndexError:
        pass

def run(directory, cds_name, output_dir):
    parts = cds_name.split('_', 3)
    cds_name = parts[-1]
    record_name = '_'.join(parts[:2])
    record = search_nbc(record_name, cds_name)
    get_region(cds_name, record, output_dir)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: %s gbk_dir smcog_number output_dir" % (sys.argv[0]))
        sys.exit(1)
    run(sys.argv[1], (sys.argv[2]), sys.argv[3])
