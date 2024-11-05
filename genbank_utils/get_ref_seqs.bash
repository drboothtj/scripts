#get reference sets from ncbi for a specific genus
#1 - get from NCBI
#2 - Extract Sequences
ls refseq/bacteria/*/*.gz | xargs -n1 gunzip
mkdir gbff
for file in `ls refseq/bacteria/*/*.gbff`; do mv $file ./gbff; done
rm -r refseq/
#3 - Convert to fasta and dereplicate
for file in gbff/*.gbff; do genbank_to -g $file -n $file.fna; done
python3 ~/git/assembly-Dereplicator/dereplicator.py --distance 0.005 . distance_005

