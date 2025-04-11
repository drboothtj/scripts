'''
convert an mmseq tsv to fast files for each cluster
'''

from collections import defaultdict
from sys import argv
from typing import List, Tuple

def write_list_to_txt(lines: List, filename: str) -> None:
    '''
    write a list to lines of a file
        arguments:
            lines: a list of lines to write
            filename: path to write to
        returns:
            None
    '''
    with open(filename, 'w') as f:
        for line in lines:
            f.writelines(line + '\n')

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
    clusters = defaultdict(list)
    biggest_cluster = 1
    biggest_name = 'ERROR'
    for pair in pairs:
        clusters[pair[0]].append(pair[1])

    biggest_name = max(clusters, key=lambda k: len(clusters[k]))
    biggest_cluster = len(clusters[biggest_name])
    print(f'The biggest cluster was {biggest_name} with a size of {biggest_cluster}.')
    for cluster in clusters:
        if len(clusters[cluster]) > 100:
            write_list_to_txt(clusters[cluster], cluster + '.txt')
            

tsv_path = argv[1]
main(tsv_path)
