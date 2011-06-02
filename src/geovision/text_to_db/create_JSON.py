# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jjlaukka"
__date__ ="$Jun 1, 2011 1:56:40 PM$"

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import Blast, Read, DbEntry, Result

results = ""
depth_limit = 4

def get_Results(ecnumber):
    objects = Result.objects.filter(ec_number = ecnumber)
    return objects

def create_json(ecnumber):
    zero_nodes = get_Results(ecnumber)
    json_file = open("/home/jjlaukka/Opiskelu/ohtuprojekti/Jit/Examples/RGraph/json_file.json", 'w')

    json_file.write("{\n")

    json_file.write("id: \"" + ecnumber + "\",\n")
    json_file.write("name: \"" + ecnumber + "\",\n")
    json_file.write("children: [" + getChildren(zero_nodes) + "]\n")

    json_file.write("}")

def get_children(ec_nodes):
    
    get_children.depth_counter += 1

    for obj in ec_nodes:
        result = result + "\t{\n\tid: \"" + obj.db_entry.read_id + "\",\n"
        result = result + "\tname: \"" + obj.db_entry.read_id + "\",\n"
        result = result + "\tdata: {\n\t\trelation: \"<h4>relations here..</h4>\"\n\t},\n"

        if get_children.depth_counter < depth_limit:
            read_children = Result.objects.filter(db_entry=obj.db_entry)
        else:
            results = results + "\tchildren: []\n\t}"
            get_children.depth_counter -= 1
            return children;


if __name__ == "__main__":
    create_json("1.2.3.22")
