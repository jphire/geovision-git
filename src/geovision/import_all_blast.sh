#!/bin/bash
BASE=/home/group/urenzyme/geoviz/blast/results

for f in $BASE/*.*
do
	echo $f
	time -p ./run.sh text_to_db/blast_parser.py $f
done
