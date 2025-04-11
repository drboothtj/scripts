'''
convert an mmseq tsv to fast files for each cluster
'''

from sys import argv
from typing import List, Tuple

def remove_duplicates(pairs: List[Tuple]) -> List[Tuple]:
    '''
    remove identical pairs by converting a list of tuples to a set
        arguments:
            pairs: a list of tuples
        returns:
            pairs: pairs with duplicates removed
    '''
    pairs = set(pairs)
    return list(pairs)

def read_two_column_tsv(tsv_path: str) -> List[Tuple]:
    '''
    read a two column tsv file and return each line as a tuple
        arguments:
            tsv_path: path to a two column csv
        returns:
            pairs: a list of tuples length 2 for each row
    '''
    read_file = open(tsv_path, "r")
    pairs = [tuple(line.strip().split("\t")) for line in read_file.readlines()]
    return pairs


def main(mmseq_path: str) -> None:
    '''
    main routine
        argument:
            mmseq_path: path to a mmseq.tsv
        returns:
            None
    '''
    pairs = read_two_column_tsv(mmseq_path)
    pairs = remove_duplicates(pairs)
    clusters = {}
    biggest_cluster = 1
    biggest_name = 'ERROR'
    for pair in pairs:
        if pair[0] in clusters.keys():
            clusters[pair[0]].append(pair[1])
        else:
            clusters[pair[0]] = [pair[1]]

    biggest_name = max(clusters, key=lambda k: len(clusters[k]))
    biggest_cluster = len(clusters[biggest_name])
    print(f'The biggest cluster was {biggest_name} with a size of {biggest_cluster}.')
    print(f'Its members are {clusters[biggest_name]}.')

tsv_path = argv[1]
main(tsv_path)
