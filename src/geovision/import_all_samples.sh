#!/bin/sh
BASE=/home/group/urenzyme/geoviz/

for f in $BASE/samples/data/*.fasta
do
#	BASENAME=`basename $f`
#	NAME=${BASENAME/.fasta/}
	echo $f
	time -p ./run.sh run_sample_parser.py $f
done
