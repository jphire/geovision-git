#!/bin/sh -x
BASE=/home/group/urenzyme/geoviz
EXCLUDE=toy

for f in $BASE/samples/data/*.fasta
do
#	BASENAME=`basename $f`
#	NAME=${BASENAME/.fasta/}
#	echo $f
	if echo "$f" | grep -v "$EXCLUDE"
	then time -p ./run.sh run_sample_parser.py $f || exit 1
	fi
done
