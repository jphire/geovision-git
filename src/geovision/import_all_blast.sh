#!/bin/bash
BASE=/home/group/urenzyme/geoviz/blast/results
EXCLUDE="silva|SRR|AAFX"

for f in $BASE/*.*.align
do
	if echo "$f" | egrep -v "$EXCLUDE"
	then
		time -p ./run.sh text_to_db/blast_parser.py $f || exit 1
	fi
done
