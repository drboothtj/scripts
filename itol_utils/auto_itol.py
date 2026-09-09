'''
a script to automatically generate an itol annotations file from a csv
    argv[1]: input .csv - two colums, ID and value
'''
import csv

from sys import argv
from typing import Dict, List
from collections import defaultdict

HEADER = [
    "DATASET_SYMBOL",
    "SEPARATOR COMMA",
    "DATASET_LABEL,label",
    "COLOR,#ffff00",
    "MAXIMUM_SIZE,10",
    "DATA",
    "#ID,symbol,size,color,fill,position,label"
]

COLOURS = [
    "#e69f00", "#56b4df", "#009e74", "#cc79a7", "#0071b2", "#d55c00", "#f0e441",
    "#ffffff", "#000000"
    ]

def read_csv(filename: str) -> List[List]:
    '''
    read a csv file into a list
        arguments:
            filename: path to .csv file
        returns:
            lines: lines as a list of lists
    '''

    with open(filename, newline="") as f:
        reader = csv.reader(f, delimiter=";")
        lines = [row for row in reader]
    return lines

def get_dictionaries(lines: List[List]) -> List[Dict]:
    '''
    read lines into values dictionaries
    for each column create a new dictionary with keys as the unique valyes
        arguments:
            lines: a list of lines (lists)
        returns:
            values_dicts: a list of dictionaries for each column
    '''
    values_dicts = []
    for x in range(1, len(lines[0])):
        #nts: defaultdict automatically creates a list
        values_dict = defaultdict(list)
        for line in lines:
            id_ = line[0]
            value = line[x]
            values_dict[value].append(id_)
        values_dicts.append(values_dict)
    return values_dicts

def get_lines(values_dict: Dict, iteration: int) -> List[str]:
    '''
    convert the values dictionary into itol readable strings, add the header and print the output
        arguments:
            values_dict: values dictionary generated when reading
        returns:
            None
    '''
    colour_id = 0
    final_lines = []

    for key, values in values_dict.items():
        lines = [
            f"{value},{iteration},50,{COLOURS[colour_id]},1,-{iteration},{key}"
            for value in values
        ]
        final_lines.extend(lines)
        colour_id += 1
    output = "\n".join(final_lines)
    print(output)

def main(filename: str) -> None:
    '''
    main routine
        arguments:
            filename: path to .csv file as string
        returns:
            None
    '''
    lines = read_csv(filename)
    values_dicts = get_dictionaries(lines)

    print("\n".join(HEADER))
    for x, values in enumerate(values_dicts):

        if len(values) > len(COLOURS):
            raise Exception(
                f"More values ({len(values)}) than colours ({len(COLOURS)})!"
                "Please add more colours or reduce the number of unique values."
                            )
        get_lines(values, x + 1) #no shape id or pos of 0

FILENAME = argv[1]
main(FILENAME)
