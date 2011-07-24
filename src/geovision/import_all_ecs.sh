#!/bin/bash -x

time ./run.sh text_to_db/uniprot_ecs_parser.py /home/group/urenzyme/geoviz/databases/uniprot/uniprot_sprot.ecs || exit 1
