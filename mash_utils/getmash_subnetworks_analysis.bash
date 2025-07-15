
#find the files corresponding to each protein
for file in *.txt; do while read line; do echo $line | cut -d '.' -f3 | cut -d '/' -f4; done < $file > $file.lof; done

#get the fasta files for each .lof
for file in *.lof; do mkdir ${file}_fa; while read line; do cp ../../data_folders/antismash_gbk/fa/derep/$line*.fa ${file}_fa; done < $file; done

#rename the dodgy dir names
for file in *_fa; do mv "$file" "${file%.txt.lof_fa}"; done


#not necissary but useful for finding the largest file
find *.lof -type f -printf '%s %p\n'|sort -nr|head

#run mmseq
~/mmseqs/bin/mmseqs easy-cluster

#find subnetworks over a certain size (remove small from txt)
for file in *.lof; do echo $file; cat $file | wc -l; done > file_size.txt

#after removing, rename something sensible
mv file_size.txt more_than_3.txt
