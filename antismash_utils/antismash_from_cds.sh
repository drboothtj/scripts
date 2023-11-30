# Takes a CDS identifier and sideloads it using antismash
# Useful for visualising areas surrounding a gene that falls outside of a detected cluster
while read cds
do 
	MYFILE=`grep $cds ~/data/g1000/*.gbk -l`
	antismash --minimal --skip-zip --sideload-by-cds $cds -v $MYFILE
done
