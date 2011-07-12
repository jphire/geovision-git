#!/bin/bash

time ./run.sh text_to_db/compound_parser.py /home/group/urenzyme/geoviz/kegg/compound || exit 1
time ./run.sh text_to_db/enzyme_parser.py /home/group/urenzyme/geoviz/kegg/enzyme || exit 1
time ./run.sh text_to_db/reaction_parser.py /home/group/urenzyme/geoviz/kegg/reaction || exit 1

