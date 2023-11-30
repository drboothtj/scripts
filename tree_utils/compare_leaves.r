###
# An R script for comparing leaves in a tree and outputting differences
# Arguments:
#	[1]: 1st tree
#	[2]: 2nd tree

library(ape)

#get args
args <- commandArgs(trailingOnly = TRUE)
tree_1_path <- as.character(args[1])
tree_2_path <- as.character(args[2])
cat('Comparing', tree_1_path, 'and', tree_2_path, "\n")

#iead trees
tree_1 <- read.tree(tree_1_path)
tree_2 <- read.tree(tree_2_path)
#cat(write.tree(tree_1), "\n")

#get leaves
tree_1_leaves <- tree_1$tip.label
tree_2_leaves <- tree_2$tip.label

#get common and unique leaves
unique_to_tree1 <- setdiff(tree_1_leaves, tree_2_leaves)
unique_to_tree2 <- setdiff(tree_2_leaves, tree_1_leaves)
#common_leaves <- intersect(tree_1_leaves, tree_2_leaves)

#print output
cat("Leaves unique to tree 1:", unique_to_tree1, "\n")
cat("Leaves unique to tree 2:", unique_to_tree2, "\n")
#cat("Common leaves:", common_leaves, "\n")

