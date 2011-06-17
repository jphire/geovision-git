#!/bin/bash
BASE=/home/group/urenzyme/geoviz/blast/result

for f in *.*
do
	FILE=$BASE$f/*.fasta
	NAME=${f/'/'/'-'}
	echo $FILE $NAME
	time ./run.sh run_sample_parser.py $FILE db $NAME
done
