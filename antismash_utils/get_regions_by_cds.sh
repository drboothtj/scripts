#finds the antismash region that a specific cds is present in
touch regions.txt
echo -n "" > regions.txt
while read cds
do
	grep $cds ./*/*region*.gbk -l | tr '\n' " " >> regions.txt
done
