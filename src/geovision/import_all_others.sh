#!/bin/bash

time ./run.sh text_to_db/enzyme_list_parser.py /home/group/urenzyme/geoviz/kegg/enzyme
time ./run.sh text_to_db/uniprot_ecs_parser.py /home/group/urenzyme/geoviz/databases/uniprot/uniprot_sprot.ecs
