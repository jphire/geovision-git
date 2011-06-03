#!/bin/sh
BASE=/home/group/urenzyme/geoviz/

for f in $BASE/samples/data/*.fasta
do
	BASENAME=`basename $f`
	NAME=${BASENAME/.fasta/}
	echo $f $NAME
	time ./run.sh run_sample_parser.py $f sample $NAME
done
