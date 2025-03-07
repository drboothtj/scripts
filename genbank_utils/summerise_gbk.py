'''
take a glob of .gbks and summerise their stats
    arguments:
        argv[1]: 
            glob string for gbks of interest
            e.g. '*.gbk'
            REMEMBER TO USE QUOTES!
'''
import glob
import statistics

from sys import argv
from typing import List
from collections import Counter

def print_size_info(sizes):
    '''
    print size range and averages to the console
        arguments:
            sizes: a list of integers
        returns:
            None
    '''
    #in a future version it would be cool to plot the histogram as an svg
    size_mean = sum(sizes) / len(sizes)
    size_median = statistics.median(sizes)
    size_deviation = statistics.stdev(sizes)
    size_min = min(sizes)
    size_max = max(sizes)

    print('--- size info ---')
    print(f'The mean size is: {size_mean}.')
    print(f'The median size is: {size_median}.')
    print(f'The standard deviation of the size is: {size_deviation}.')
    print(f'The range of sizes is: {size_min} - {size_max}.')

def print_topology_info(topologies):
    '''
    print the topology distribution to the console
        arguments:
            topologies: a list of strings reprisenting the topologies
        returns:
            None
    '''
    total = len(topologies)
    counts = Counter(topologies)

    print('--- topology info ---')
    for item, count in counts.items():
        percentage = (count / total) * 100
        print(f"{count} sequences have {item} topologies ({percentage:.2f}%)")

def get_header_from_tsv(path):
    '''
    takes the first line of a tsv file and returns it as a list of its components
        arguments:
            path: path to the .tsv file
        returns:
            header:
                list of tab-seperated components from the first line of the file
    '''
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readline().strip().split(' ')
        lines = [item for item in lines if item != '']
        return lines

def get_details_from_gbk_header(path: str):
    '''
    get the size and topology from the header of a genbank file
        arguments:
            path: path to the genbank file
        returns:
            size:
                the length of the DNA in bp
            topology:
                whether the DNA is circular or linear
    '''
    #NB: This can be updated to include other info as needed.
    header = get_header_from_tsv(path)
    size = int(header[2]) #make sure to redefine data types to avoid problems later on!
    topology = str(header[5])
    return size, topology

def main(gbks: List):
    '''
    main routine for summerise gbks
        arguments:
            gbks: glob string for genbank files
    '''
    paths = glob.glob(gbks)
    sizes = []
    topologies = []
    for path in paths:
        size, topology = get_details_from_gbk_header(path)
        sizes.append(size)
        topologies.append(topology)
    print_size_info(sizes)
    print_topology_info(topologies)

GBKS = argv[1]
main(GBKS)
