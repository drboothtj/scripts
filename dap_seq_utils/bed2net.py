'''
Take a glob of .bed files and produce a draft transcriptional network
    requires: networkx
    parameters:
        argv [1]: mapping file,
            a two-column csv (semi-colons) with filenames linked to the protein the reprisent
            e.g. each row(protein1_assigned_genes.bed; Protein1)
            this is necissary because filenames from DAP-seq pipeline are often very complex
            just ensure the paths are correct and the protein names are EXACTLY as they appear
            in the 'locus_tag=' column of the .bed
'''
from sys import argv
from typing import List, Tuple

import csv
import re

import networkx as nx
import matplotlib.pyplot as plt

def plot_png(network: nx.DiGraph) -> None:
    '''
    plot a png from a networkx graph (ugly!)
        arguments:
            network:
                directed graph from networkx
        returns:
            None
    '''
    regulators = [n for n, d in network.nodes(data=True) if d.get('type') == 'regulator']
    genes = [n for n, d in network.nodes(data=True) if d.get('type') != 'regulator']
    pos = nx.spring_layout(network, seed=42)
    nx.draw_networkx_nodes(
        network, pos, nodelist=regulators, node_color='red', node_size=500,
        )
    nx.draw_networkx_nodes(
        network, pos, nodelist=genes, node_color='lightblue', node_size=500, label='Genes'
        )
    nx.draw_networkx_edges(network, pos, arrows=True)
    nx.draw_networkx_labels(network, pos, font_size=8)
    plt.figure(figsize=(12, 12))
    plt.legend(scatterpoints=1)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("network.png", dpi=300)
    plt.show()

def read_bed(filepath:str) -> List:
    '''
    read a .bed file and extract the locus tags
        arguments:
        returns:
    '''
    locus_tags = []
    pattern = re.compile(r"locus_tag=([^;]+)")
    filepath = filepath.lstrip('\ufeff').strip() #remove windows garbage
    with open(filepath, "r") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                locus_tags.append(match.group(1))
    return locus_tags

def generate_network(mapping: List[Tuple]) -> nx.DiGraph:
    '''
    generate a directed network from the mapping file
        arguments:
            mapping: the list of Tuples from the mapping file
        returns: 
            Graph: the digraph object from networkx

    '''
    network = nx.DiGraph()
    for filepath, source_protein in mapping:
        if source_protein not in network:
            network.add_node(source_protein, type='regulator')
        else:
            network.nodes[source_protein]['type']='regulator'
        target_proteins = read_bed(filepath)
        for target in target_proteins:
            network.add_node(target)  # Safe to call even if exists
            network.add_edge(source_protein, target)
    return network

def read_map(mapping_file: str) -> List[Tuple]:
    '''
    read mapping file, return a list of tuples
        arguments:
            mapping_file: path to mapping file
        returns:
            mapping: Tuple containing the file name and the protein name
    '''
    mapping_items = []
    with open(mapping_file, 'r', newline='') as file:
        reader = csv.reader(file, delimiter =';')
        for row in reader:
            if len(row) == 2:  # ensure exactly two columns
                mapping_items.append((row[0].strip(), row[1].strip()))
            else:
                raise Exception(
                    'The mapping file is not formatted correctly. '
                    'Please ensure you have provided a .csv with two columns per row.'
                    f'See: "{row}".')
    return mapping_items

def main(mapping_file: str):
    '''
    main routine
        args: 
            files: str reprisenring the path to .bed files
    '''
    mapping = read_map(mapping_file)
    network = generate_network(mapping)
    nx.write_graphml(network, "bed2net.graphml")
    plot_png(network)

MAPPING_FILE = argv[1]
main(MAPPING_FILE)
