'''
get clusters as simple .txt files from cd-hit output
'''
import os

from sys import argv
from typing import List

def write_lines(lines: List[str], filename:str) -> None:
    '''
    write a list of strings to a file
        arguments: lines: lines to write
        filename: path  to write file
    '''
    with open(filename, 'w') as writefile:
        for line in lines:
            writefile.writelines(line + '\n')

def read_lines(filename) -> List[str]:
    '''
    read lines from a text file
        arguments:
            filename: path to .txt
    '''
    with open(filename, 'r') as readfile:
        lines = readfile.readlines()
    return lines

def write_clusters(lines: List[str]) -> None:
    '''
    read and write clusters from cd-hit lines
        arguments:
            lines: lines from cd-hit output as list
    '''
    clusters = []
    cluster_dict = None
    for line in lines: #this construction is terrible - sorry!
        if line[0] == '>':
            if cluster_dict:
                clusters.append(cluster_dict)
            filename = line [1:-1]
            filename = (''.join(filename.split()) + '.txt').lower()
            cluster_dict = {
                'name' : filename,
                'ids' : []
            }
        if line[0].isnumeric():
            newline = (line.strip().split()[2].lstrip('>').rstrip('.'))
            cluster_dict['ids'].append(newline)
    clusters.append(cluster_dict) #catch the last one
    for cluster in clusters:
        write_lines(cluster['ids'], cluster['name'])


def main(filename: str) -> None:
    '''
    main routine
        arguments:
            filename: path to cd-hit output
    '''
    lines = read_lines(filename)
    write_clusters(lines)

filename = argv[1]
main(filename)

