#Get genomes from NCBI and deteplicate
#Requirements: mash, assembly-Dereplicator, genbank_to
#Note: needs testing!

#ncbi-genome-download --genera burkholderia --assembly-levels complete bacteria
echo 'Step 2: Cleaning Data'
#ls refseq/bacteria/*/*.gz | xargs gunzip
#mkdir gbff
#for file in refseq/bacteria/*/*.gbff; do mv $file gbff; done
#rm -r refseq

#echo 'Step 3: Converting to .fna'
#for file in gbff/*.gbff; do genbank_to -g $file -n $file.fna; done
#mkdir fna
#mv gbff/*.fna fna/.

echo 'Step 4: Dereplicating'
#python3 ~/git/assembly-Dereplicator/dereplicator.py --distance 0.005 ./fna distance_005
#mkdir set_1 set_2 set_3
cd distance_005
ls | sort -R | head -n 100 | xargs -I x mv x ../set_1
ls | sort -R | head -n 100 | xargs -I x mv x ../set_2
ls | sort -R | head -n 100 | xargs -I x mv x ../set_3
