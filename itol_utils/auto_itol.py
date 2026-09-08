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

def read_csv_to_dict(filename: str) -> Dict:
    '''
    read a csv file into a dictionary where the keys are unique values
        arguments:
            filename: path to .csv file
        returns:
            values_dict: dictionary of unique values
    '''
    #nts: defaultdict automatically creates a list
    values_dict = defaultdict(list)

    with open(filename, newline="") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            id_, value = row
            values_dict[value].append(id_)

    return values_dict

def get_lines(values_dict: Dict) -> List[str]:
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
            f"{value},2,50,{COLOURS[colour_id]},1,-1,{key}"
            for value in values
        ]
        final_lines.extend(lines)
    output = "\n".join(HEADER + final_lines)
    print(output)

def main(filename: str) -> None:
    '''
    main routine
        arguments:
            filename: path to .csv file as string
        returns:
            None
    '''
    values = read_csv_to_dict(filename)

    if len(values) > len(COLOURS):
        raise Exception(
            f"More values ({len(values)}) than colours ({len(COLOURS)})!"
            "Please add more colours or reduce the number of unique values."
                        )

    get_lines(values)

FILENAME = argv[1]
main(FILENAME)
