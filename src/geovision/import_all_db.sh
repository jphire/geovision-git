#!/bin/bash
BASE=/home/group/urenzyme/geoviz/databases/

for f in uniprot silva/lsu silva/ssu frnadb
do
	FILE=$BASE$f/*.fasta
	NAME=${f/'/'/'-'}
	echo $FILE $NAME
	time ./run.sh run_db_parser.py $FILE "$NAME"
done
