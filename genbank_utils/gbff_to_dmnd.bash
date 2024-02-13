### create a diamond database from a bunch of .gbff files
#convert to .fna
for file in `ls *.gbff`;
do genbank_to -g $file -a $file.faa;
done

#cat_files
cat *.faa > cat.faa

#make diamond db
diamond makedb --in cat.faa -d dmnd.dmnd


