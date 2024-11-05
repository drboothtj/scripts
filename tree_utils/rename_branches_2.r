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
		print(file)
		tree <- read.tree(file)
		tip_labels <- tree$tip.label
		tips <- c()
		for (tip in tip_labels){
			split_tip <- strsplit(tip, "\\.")[[1]]
			tips <- append(tips, split_tip[1])
		}
		tree$tip.label <- tips
		new_filename <- paste('new', file, sep ='_')
		write.tree(tree, new_filename)
}
