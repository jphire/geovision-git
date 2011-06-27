#!/bin/bash
BASE=/home/group/urenzyme/geoviz/blast/results

for f in $BASE/*.*.align
do
	echo $f
	if echo "$f" | grep -v silva
	then
		time -p ./run.sh text_to_db/blast_parser.py $f
	fi
done
