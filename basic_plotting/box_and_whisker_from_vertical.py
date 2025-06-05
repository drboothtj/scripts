'''
make strip plot svgs from vertical columed data
'''
import csv
import random
from sys import argv

import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

def get_data_from_csv(filename):
    '''
    get data for strip plot from file
        arguments:
            filename: path to columned .csv
    '''
    lines = []
    with open(filename, 'r') as readfile:
        reader = csv.reader(readfile, delimiter=";")
        for line in reader:
            lines.append(line)
    return lines

def plot_strip_plot(headers, data):
    '''
    make a strip plot from data
    '''
    fig, ax = plt.subplots()
    '''
    for i, category in enumerate(headers):
        #plot data by category
        values = data[i]
        jitter_amount = 0.3
        x_positions = [i + random.uniform(-jitter_amount, jitter_amount) for _ in values]  
        ax.scatter(x_positions, values, alpha=1, s=0.1)
        #also calculate mean
        mean_value = np.mean(values)
        ax.scatter(i, mean_value, color='black', marker='x', s=100, linewidths=2, label='Mean')
    '''
    # Boxplot overlay — position is important
    ax.boxplot(
        [np.array(data[i], dtype=float) for i in range(len(headers))],
        positions=range(len(headers)),
        widths=0.3,
        patch_artist=True,
        boxprops=dict(facecolor='none', color='black'),
        medianprops=dict(color='red'),
        whiskerprops=dict(color='black'),
        capprops=dict(color='black'),
        flierprops=dict(marker='o', markersize=2, alpha=0.3)
    )


    plt.xticks(range(len(headers)), headers)
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.title('Strip Plot Using Pure Matplotlib')
    plt.savefig('strip.png')

def main(filename):
    '''
    main routine
        argument:
            filename: path to .csv
    '''
    data = get_data_from_csv(filename)
    headers = data[0]
    rows = data[1:]
    transposed_rows = [
        [float(row[i]) for row in rows if row[i] != ''] for i in range(len(rows[0]))
    ]
    plot_strip_plot(headers, transposed_rows)

mpl.rcParams['figure.dpi'] = 600
filename = argv[1]
main(filename)
