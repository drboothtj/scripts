'''
A tool for clustering trees by RF scores. The first half of this script is duplicated from treeoutliers.py

Arguments:
    argv[1]: list of taxa as a .txt file
    argv[2:]: tree files to be compared
'''
import os
import glob
import matplotlib.pyplot as plt
import statistics as stats
from sys import argv
from ete3 import Tree
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

def read_taxa(filename):
    '''
    get the list of taxa from a .txt file.
        arguments:
            filename: the path to the .txt file
        returns:
            taxa: a list of taxa
    '''
    with open(filename, 'r') as f:
        taxa = f.readlines()
    return taxa

def read_tree(filename):
    '''
    read a tree from a file and return its name and structure
        arguments:
            filename: the path to a newick tree file
        returns:
            tree_name: name of the tree file minus path
            tree_structure: newick structure of the tree as a string
    '''
    tree_name = os.path.splitext(os.path.basename(filename))[0]
    with open(filename) as f:
        tree_structure = f.read()
    return tree_name, tree_structure

def rename_branches(tree, taxa):
    '''
    takes a newick tree and swaps the taxa name with the shorter name from the taxa list
        arguments:
            tree: tree in newick format
            taxa: list of taxa from the file
        returns:
            tree:
                tree with renamed leaves
    '''
    for leaf in tree:
        for taxon in taxa:
            #print(f'{taxon} vs. {leaf.name}')
            if leaf.name.strip().startswith(taxon.strip()):
                leaf.name = taxon
    return tree

#get file names from args
files = []
for arg in argv[2:]: #handel wildcards without needing quotes
	files.extend(glob.glob(arg))

#get taxa from .txt
taxa_filename = argv[1]
taxa= read_taxa(taxa_filename)

#get tree from each file
trees = []
for tree_file in files:
    tree_name, tree_structure = read_tree(tree_file)
    try:
        tree_structure = Tree(tree_structure)
    except:
        raise(f'{tree_name} cannot be read by ete3. Check if the tree is formatted correctly.')
#   tree_structure = rename_branches(tree_structure, taxa)
    tree_dict = {
        'name' : tree_name,
        'structure': tree_structure
    }
    trees.append(tree_dict)

#compare all trees
for tree1 in trees:
    rf_scores = []
    for tree2 in trees:
        if tree1['name'] == tree2['name']:
            pass
        else:
            ete_tree1 = tree1['structure']
            ete_tree2 = tree2['structure']
            score = ete_tree1.robinson_foulds(ete_tree2, unrooted_trees='True')
            percentage_similarity = (1 - score[0]/score[1]) * 100
            rf_scores.append(percentage_similarity)
    tree1['scores'] = rf_scores

#do elbow plot
all_scores = []
for tree in trees:
    all_scores.append(tree['scores'])
sum_of_squares = []
k_values = range(1,10) 
for k in k_values:
    kmeans = KMeans(n_clusters=k, n_init = 10)
    kmeans.fit(all_scores)
    sum_of_squares.append(kmeans.inertia_)

#plot
plt.figure(figsize=(8, 4))
plt.plot(k_values, sum_of_squares, marker='o', linestyle='-', color='b')
plt.title('Elbow Plot for K-means Clustering')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.xticks(k_values)
plt.grid(True)
plt.savefig('elbow.png')

#calculate
kmeans = KMeans(n_clusters=2, n_init = 10)
cluster_labels = kmeans.fit_predict(all_scores)

plt.figure(figsize=(8, 6))
# Create a scatter plot for each cluster
for cluster_id in range(2):  # Change this to match the number of clusters (K)
    cluster_data = np.array(all_scores)[cluster_labels == cluster_id]  # Extract data points in the current cluster
    plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {cluster_id + 1}')  # Use [:, 0] and [:, 1] for the two features
plt.savefig('clusters.png')

# do PCA


#plot PCA
#note: we do not need to scale our data as all dimensions are in the same scale (%)

pca_data = np.array([tree['scores'] for tree in trees])
pca = PCA(2)
principal_components = pca.fit_transform(pca_data)
plt.figure(figsize=(8, 6))
plt.scatter(principal_components[:, 0], principal_components[:, 1])
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA Plot')
plt.savefig('pca.png')

explained_variance_ratios = pca.explained_variance_ratio_

# Calculate the cumulative explained variance
cumulative_variance = np.cumsum(explained_variance_ratios)
print("Explained Variance Ratios:")
for i, ratio in enumerate(explained_variance_ratios):
    print(f"PC{i + 1}: {ratio:.2f}")
