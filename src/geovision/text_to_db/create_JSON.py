# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jjlaukka"
__date__ ="$Jun 1, 2011 1:56:40 PM$"

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import Blast, Read, DbEntry, Results

def get_Results(ecnumber):
    objects = Results.objects.filter(ec_number=ecnumber)
    return objects

def create_json(self, ecnumber):
    center_nodes = get_Results(ecnumber)
    db_children= get_db_children(center_nodes)


def get_db_children(nodes):
    results = []
    for obj in nodes:
        results.append(DbEnty.objects.get)

def get_read_children(self, db):
    return Read.objects.filter()

def get_ec_children(self, db):
    return Results.objects.filter(db_entry.r)

if __name__ == "__main__":
    create_json(ecnumber)
