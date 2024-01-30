### An R script for renaming leaves, specifically it cuts on a specific character
### This is used to make names uniform for building consensus trees
### Trees must be in the current directory 
### cuts on "." hard coded because regex.. hard coded because regex..-

library(ape)

#get args
args <- commandArgs(trailingOnly=TRUE)
#cut_character <- as.character(args[1])
cut_character <- "."

#get files
files <- list.files('.')

#rename leaves
for (file in files)
	{
		tree <- read.tree(file)
		tip_labels <- tree$tip.label
		#print(tip_labels)
		cut_labels <- strsplit(tip_labels, "\\.")
		final_labels <- sapply(cut_labels, function(x) x[1])
		#print(final_labels)
		tree$tip.label <- final_labels
		new_filename <- paste('new', file, sep ='_')
		write.tree(tree, new_filename)

}
