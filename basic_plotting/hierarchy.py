'''
takes a feature table and produces hierarchical clusters
    argv[1]: path to .csv
    argv[2]: float for clustering cutoff (def. 0.5), bigger means more relaxed
'''
from sys import argv

import csv
import numpy as np
import matplotlib.pyplot as plt

from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist


def read_feature_table(file_path):
    '''
    reads a feature table.csv and return and array and its labels
        arguments:
            file_path: path to feature table .csva
    '''
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header if present
        labels = []
        data = []
        for row in reader:
            labels.append(row[0])
            data.append([int(x) for x in row[1:]])
    return labels, np.array(data)

def get_jaccard_matrix(data):
    '''
    take a numpy table with binary data and calculate jaccard linkage
        arguments:
            data: numpy array with binary observations
        returns:
            j_matrix: matrix of the jaccard distances
    '''
    distance_matrix = pdist(data, metric='jaccard')
    j_matrix = linkage(distance_matrix, method='average')
    return j_matrix

def plot_dendrogram(matrix, output) -> None:
    '''
    plot a dendrogram from a linkage matrix
        argument:
            matrix: linkage matrix from scipy
            output: path for output .png
    '''
    plt.figure(figsize=(10, 6))
    dendrogram(matrix)
    plt.title("Hierarchical Clustering of Binary Data")
    plt.xlabel("Sample Index")
    plt.ylabel("Jaccard Distance")
    plt.tight_layout()
    plt.savefig(output)
    plt.close()

def write_clusters(matrix, labels, t, output):
    '''
    get clusters from matrix and write to .tsv
    '''
    clusters = fcluster(matrix, t=t, criterion='distance') #adjust t for different clustering
    with open(output, "w", newline='') as out:
        writer = csv.writer(out, delimiter='\t')
        writer.writerow(["Sample", "Cluster"])
        for label, cluster_id in zip(labels, clusters):
            writer.writerow([label, cluster_id])

def main(filename, t_value):
    '''
    main routine
        arguments:
            filename: path to .csv file
            t_value: distance threshold to calculate clusters
    '''
    labels, data = read_feature_table(filename)
    j_matrix = get_jaccard_matrix(data) #Jaccard distance is used for binary data
    plot_dendrogram(j_matrix, 'hierarchy.png') #add output argument when a parser is made....
    write_clusters(j_matrix, labels, t_value, "clusters.csv")  #see above

filename = argv[1]
print(len(argv))
if len(argv) < 3:
    t_value = 0.5
else:
    t_value = argv[2]
main(filename, t_value)
