# Rscript to produce tanglegrams from two unrooted trees (trees will be rerooted by midpoint)
# Arguments:
#   args[1]: path to the first tree
#   args[2]: path to the second tree
#   args[3]: path to a list of ids to colour

# install libraries
#install.packages(c("phytools", "paco", "plotly", "viridis", "svglite"))

# get libraries
library(phytools)
library(paco)
library(plotly)
library(viridis)
library(svglite)
library(colorspace)

# get arguments
args <- commandArgs(trailingOnly = TRUE)
tree_1_path <- args[1]
tree_2_path <- args[2]
metadata_files <- if (length(args) >= 3) args[3:length(args)] else character(0)

# Get base names of the trees (removes directory)
tree_1_base <- tools::file_path_sans_ext(basename(tree_1_path))
tree_2_base <- tools::file_path_sans_ext(basename(tree_2_path))
output <- paste0(tree_1_base, "_vs_", tree_2_base, ".svg")

# preprocess genome tree
tree_1 <- read.tree(tree_1_path)
# midpoint root
tree_1 <- phangorn::midpoint(tree_1)
tree_1 <- ladderize(reorder(tree_1))

# preprocess bgc tree
tree_2 <- read.tree(tree_2_path)
# midpoint root
tree_2 <- phangorn::midpoint(tree_2)
tree_2 <- ladderize(reorder(tree_2))

# build links, here it mapped the same genome_ids
links <- cbind(tree_2$tip, tree_2$tip)
red_cb <- rgb(213/255,94/255,0)
link_colors <- rep(red_cb, nrow(links))
obj <- cophylo(tree_1, tree_2, links, rotate = TRUE)

##manage metadata files##
# read groups into a list
metadata_list <- lapply(metadata_files, function(f) scan(f, what=character(), quiet=TRUE))

#get colours
green_cb <- rgb(0,158/255,115/255)
yellow_cb <- rgb(240/255,228/255,66/255)
for (i in seq_along(metadata_list)) {
  ids <- metadata_list[[i]]
  if (i == 1) {
    link_colors[links[,1] %in% ids] <- green_cb
  } else if (i == 2) {
    link_colors[links[,1] %in% ids] <- yellow_cb
  } 
  # add more conditions if needed
}

# create svg
svglite(output, width = 16, height = 16)
# draw the cophylo
plot.cophylo(obj, link.type="curved", link.lwd=4, link.lty="solid", fsize=c(2.25,2.25), pts=FALSE, link.col = link_colors, edge.lwd=4)

nodelabels.cophylo(obj$trees[[1]]$node.label[2:Nnode(obj$trees[[1]])],
  2:Nnode(obj$trees[[1]])+Ntip(obj$trees[[1]]),frame="none",
  cex=2,adj=c(1,-0.4),which="left")

nodelabels.cophylo(obj$trees[[2]]$node.label[2:Nnode(obj$trees[[2]])],
  2:Nnode(obj$trees[[2]])+Ntip(obj$trees[[2]]),frame="none",
  cex=2,adj=c(0,1.4),which="right")

## add tip labels
tiplabels.cophylo(pch=NA,frame="none", cex=2) #bg=tip_colors1,cex=1.5)
tiplabels.cophylo(pch=NA,frame="none", cex=2) #bg=tip_colors2,which="right",cex=1.5)

all(links[,1] %in% tree_1$tip.label)
all(links[,2] %in% tree_2$tip.label)
cat("SVG written to", output, "\n")
