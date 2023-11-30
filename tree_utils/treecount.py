'''
a python script to count individual support values. Used for small numbers of consensus trees.
	arguments:
		argv[1]: path to the tree file
'''
import sys
from Bio import Phylo
from collections import Counter

#get path and read tree
filename = sys.argv[1]
tree = Phylo.read(filename, "newick")

#get support values and remove None values
support_values = [clade.confidence for clade in tree.find_clades()]
#support_values = [value for value in support_values if value is not None]

#count values and print
counter = Counter(support_values)
print(sum(counter.values()))
print(counter)

