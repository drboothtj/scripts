'''
convert an mmseq tsv to fast files for each cluster
'''

from sys import argv
from typing import List, Tuple, Set

def get_representatives(pairs):
    '''
    get a list of reprisentative sequences
    '''
    reprisentatives = {pair[0] for pair in pairs}
    return list(reprisentatives) #return the set as a list for faster iteration

def remove_duplicates(pairs: List[Tuple]) -> Set[Tuple]:
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
            mmseq_path: path to a mmseq .tsv
        returns:
            None
    '''
    pairs = read_two_column_tsv(mmseq_path)
    pairs = remove_duplicates(pairs)
    representatives = get_representatives(pairs)
    number_of_clusters = len(representatives)
    cluster_sizes = []
    #convert reps to dict.
    for pair in pairs:
        members = [pair[1] for pair in pairs if pair[0]==rep] #reverse to loop over reps instead? #set inscetion between reps
        cluster_sizes.append(len(members))
    print(
        f'there are {number_of_clusters} clusters'
        f'ranging from {min(cluster_sizes)} to {max(cluster_sizes)}'
    )

tsv_path = argv[1]
main(tsv_path)