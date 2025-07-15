#renames fasta put together from: 
#for file in *.fa; do head $file -n2; done
#arguments: 
#         $1 : filename

sed -n '
/^==>/ {
  s/^==> \(.*\)\.txt\.fa <==$/>\1/;
  p;
  n;
  s/.*-//;
  p;
}
' $1 > $1_renamed.fa
