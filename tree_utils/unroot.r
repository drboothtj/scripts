### Unroot a newick tree
library(ape)

args <- commandArgs(trailingOnly = TRUE)
tr <- read.tree(args[1])
unrooted_tree <- unroot(tr)
write.tree(unrooted_tree, 'am_unrooted.tree')
