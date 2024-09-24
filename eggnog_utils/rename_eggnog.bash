## a bash script to rename eggnog mappers horrible names

for file in `ls *.annotations`;
  do new_name=$(echo $file | awk -F'[_.]' '{print $2"_"$3}');
  mv $file $new_name.annotations
done

