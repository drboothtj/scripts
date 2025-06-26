# not for public consumption...
# bash script for converting mmseq dual column into cluster.txts
# arguments: $1 - path to genome faas
mkdir genomes
for file in *.txt; do while read line; do echo $line; grep $line $1 | cut -d '.' -f3 | cut -d '/' -f2; done < $file > genomes/$file; done
