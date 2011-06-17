#!/bin/bash
BASE=/home/group/urenzyme/geoviz/build/results

for f in $BASE/*.build
do
	echo $f
	time ./run.sh text_to_db/build_parser.py $f
done
