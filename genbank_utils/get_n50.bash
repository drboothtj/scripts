### uses genbank to to convert a genbank to fna and then uses assembly_stats to get n50 info
### arg $1: path to genbank file
genbank_to -g "$1" -n nuc.fna
assembly_stats nuc.fna

