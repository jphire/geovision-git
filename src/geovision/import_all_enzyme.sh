#!/bin/bash -x

time ./run.sh meta/compound_parser.py /home/group/urenzyme/geoviz/kegg/compound || exit 1
time ./run.sh meta/enzyme_parser.py /home/group/urenzyme/geoviz/kegg/enzyme || exit 1
time ./run.sh meta/reaction_parser.py /home/group/urenzyme/geoviz/kegg/reaction || exit 1

