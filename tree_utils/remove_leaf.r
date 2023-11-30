### an r script to remove a given leaf from a tree
# 	args:
# 		[1]: path to tree file
#		[2]: leaf to remove

library(ape)

#get args
args <- commandArgs(trailingOnly = TRUE)
tree_path <- as.character(args[1])
tip_to_remove <- as.character(args[2])

#read tree
tree <- read.tree(tree_path)

#remove tip from tree
cat('Removing', tip_to_remove, 'from', tree_path, "\n")
if (tip_to_remove %in% tree$tip.label) {
	tree <- drop.tip(tree, tip_to_remove)
	write.tree(tree, 'leaf_removed.tree')
} else {
	cat(tip_to_remove, ' is not present in', tree_path, "\n")
}

