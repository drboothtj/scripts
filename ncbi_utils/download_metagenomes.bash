# step-by step to download metagenomes from genbank
# adapted from: http://metagenomics.wiki/tools/fastq/ncbi-ftp-genome-download

#1. get list of available 
rsync -t -v rsync://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_genbank.txt ./

#also for refseq if high-quality is needed:
#"rsync -t -v rsync://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt ./"

#2. filter for metagenomes and trim columns
cat assembly_summary_genbank.txt | cut -f 8,9,14,15,16,20 | grep metagenome > metagenomes_tbl.tsv

#3. extract ftp links
cat metagenomes_tbl.tsv | cut -f6 > ftp_links.txt

# for .gbff you can just substitute
# e.g.  sed 's/GCA/GCF/g' ftp_addresses.txt > gbff_adresses.txt
# sed 's/gff/gbff/g' ftp_addresses.txt > gbff_adresses.txt

#set up a shell script for downloading (DO IT IN SCREEN!)
awk 'BEGIN{FS=OFS="/";filesuffix="genomic.gff.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print "rsync -t -v "ftpdir,file" ./"}' ftp_links.txt | sed 's/https/rsync/g' > download_gff_files.sh

#you can also donwload, say .fna
# awk 'BEGIN{FS=OFS="/";filesuffix="genomic.fna.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print "rsync -t -v "ftpdir,file" ./"}' ftp_links.txt | sed 's/https/rsync/g' > download_fna_files.sh

#4. do the download
source download_fna_files.sh


