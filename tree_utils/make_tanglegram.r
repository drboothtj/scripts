# Rscript to produce tanglegrams from two unrooted trees (trees will be rerooted by midpoint)
# Arguments:
#   args[1]: path to the first tree
#   args[2]: path to the second tree
#   args[3]: [UNUSED] path to metadata table
#   args[4]: path for output .svg

# install libraries
#install.packages(c("phytools", "paco", "plotly", "viridis", "svglite"))

# get libraries
library(phytools)
library(paco)
library(plotly)
library(viridis)
library(svglite)

# get arguments
args <- commandArgs(trailingOnly = TRUE)
tree_1_path <- args[1]
tree_2_path <- args[2]
metadata_path <- args[3]
output <- args[4]

# read metadata table
#data <- read.csv("/home/azureuser/datadrive/saccharopolyspora_dataset/data/processed/Staphylobactin_bigfam/tables/df_gtdb_meta.csv")

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
obj <- cophylo(tree_1, tree_2, links, rotate = TRUE)

# Create a unique color for each family category.
#family_levels <- unique(data$Family)
#colors <- rainbow(length(family_levels))

# Create a named vector of colors for each family.
#family_colors <- setNames(colors, family_levels)

# Assuming 'tree_bgc$tip.label' can be matched to 'data$tip_label' to find the genus.
#tip_family1 <- data$Family[match(obj$trees[[1]]$tip.label, data$genome_id)]
#tip_colors1 <- family_colors[tip_family1]

# Assuming 'tree_bgc$tip.label' can be matched to 'data$tip_label' to find the genus.
#tip_family2 <- data$Family[match(obj$trees[[2]]$tip.label, data$genome_id)]
#tip_colors2 <- family_colors[tip_family2]

# Assuming 'tree_bgc$tip.label' can be matched to 'data$tip_label' to find the genus.
#link_family <- data$Family[match(links[,1], data$genome_id)]
#link_colors <- family_colors[link_family]

#pdf("tanglegram.pdf", width=16, height=24)
svglite(output, width = 16, height = 16)
# draw the cophylo
plot.cophylo(obj, link.type="curved", link.lwd=2, link.lty="solid", fsize=c(0.1,0.1), pts=FALSE)
             #,link.col = make.transparent(link_colors, 0.5))

nodelabels.cophylo(obj$trees[[1]]$node.label[2:Nnode(obj$trees[[1]])],
  2:Nnode(obj$trees[[1]])+Ntip(obj$trees[[1]]),frame="none",
  cex=0.5,adj=c(1,-0.4),which="left")

nodelabels.cophylo(obj$trees[[2]]$node.label[2:Nnode(obj$trees[[2]])],
  2:Nnode(obj$trees[[2]])+Ntip(obj$trees[[2]]),frame="none",
  cex=0.5,adj=c(0,1.4),which="right")

## add tip labels
tiplabels.cophylo(pch=21,frame="none", cex=1.5) #bg=tip_colors1,cex=1.5)
tiplabels.cophylo(pch=21,frame="none", cex=1.5) #bg=tip_colors2,which="right",cex=1.5)

# Use locator to interactively place the legend
# Note: Remove this line if you're running the script non-interactively or if you're saving to PDF
#position <- locator(1)  # Click on the plot where you want the legend to appear

# Add a legend outside the plot area (to the right)
#par(xpd=TRUE)  # Allow plotting outside the plot area
#legend(x="bottomleft", inset=c(-0.0, 0),  # Adjust inset to move the legend to the left
#       legend=names(family_colors), 
#       fill=family_colors, 
#       title="Family", 
#       cex=0.7, 
#       pt.cex=0.7, 
#       text.width=0.2)
