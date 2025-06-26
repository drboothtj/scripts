'''
clean and annotate me!
'''
import numpy as np
import csv
from scipy.cluster.hierarchy import linkage, dendrogram, optimal_leaf_ordering
import matplotlib.pyplot as plt
import seaborn as sns

# Load binary data from CSV (no pandas)
filename = "output.csv"

labels = []
data_matrix = []

with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)[1:]  # Skip 'Node'

    for row in reader:
        labels.append(row[0])  # Node label
        binary_row = list(map(int, row[1:]))
        data_matrix.append(binary_row)

# Perform hierarchical clustering
Z = linkage(data_matrix, method='ward')  # or 'average', 'complete', etc.

# Plot dendrogram
plt.figure(figsize=(10, 6))
dendrogram(Z, labels=labels, leaf_rotation=90)
plt.title("Hierarchical Clustering of Binary Data")
plt.xlabel("Node")
plt.ylabel("Distance")
plt.tight_layout()
plt.savefig("binary_dendrogram.png", dpi=300)
plt.close()

####and also
# Convert to NumPy array for seaborn
data_array = np.array(data_matrix)
# Create a clustermap
sns.set(font_scale=1.0)
g = sns.clustermap(data_array,
                   cmap="Blues",       # or 'binary', 'Greys', etc.
                   row_cluster=True,
                   col_cluster=True,
                   xticklabels=headers,
                   yticklabels=labels,
                   figsize=(10, 8))

plt.savefig("clustered_binary_heatmap.png", dpi=300)
plt.close()
