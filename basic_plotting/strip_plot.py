'''
make strip plot svgs from vertical columed data
'''
import csv
import random
from sys import argv

import matplotlib.pyplot as plt

def get_data_from_csv(filename):
    '''
    get data for strip plot from file
        arguments:
            filename: path to columned .csv
    '''
    lines = []
    with open(filename, 'r') as readfile:
        reader = csv.reader(readfile)
        for line in reader:
            lines.append(line)
    return lines

def plot_strip_plot(headers, numeric_rows):
    '''
    make a strip plot from data
    '''
    for col_idx, col_name in enumerate(headers):
        col_values = [row[col_idx] for row in numeric_rows]
        # jitter adds some x varience to the plots
        x_jittered = [col_idx + random.uniform(-0.1, 0.1) for _ in col_values]
        plt.scatter(x_jittered, col_values, label=col_name)

    plt.xticks(range(len(headers)), headers)
    plt.ylabel('Value')
    plt.title('Strip Plot Using Matplotlib')
    plt.tight_layout()
    plt.savefig('strip.svg')

def main(filename):
    '''
    main routine
        argument:
            filename: path to .csv
    '''
    data = get_data_from_csv(filename)

    headers = data[0]
    rows = data[1:]
    numeric_rows = [[int(value) for value in row] for row in rows]
    plot_strip_plot(headers, numeric_rows)

filename = argv[1]
main(filename)
