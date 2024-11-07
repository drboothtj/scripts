#!/usr/bin/env bash
# build a hmm model and search in one shot
#       Arguments:
#               $1: path to .msa file
#               $2: path to dir containing files to be searched - include last slash (e.g. ../faa/)
hmmbuild $1.hmm $1
for file in `ls $2`
do hmmsearch --tblout $file.tbl $1.hmm $2$file
done
