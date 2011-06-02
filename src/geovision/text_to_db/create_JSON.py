# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jjlaukka"
__date__ ="$Jun 1, 2011 1:56:40 PM$"

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import Blast, Read, DbEntry, Result

results = ""
depth_limit = 3

#THE DOUBLE UNDERSCORE CAN BE INEFFICIENT BECAUSE OF JOINS IN THE BACKGROUND: MAYBE HAVE TO BE CHANGED
#IN THE FUTURE!!!

def get_ec_results(ecnumber, limit):
    return Result.objects.filter(ec_number = ecnumber, bitscore__gt = limit)

def get_db_results(db_entry_id, limit):
    return Result.objects.filter(db_entry__read_id = db_entry_id, bitscore__gt = limit)

def get_rd_result(read_id, limit):
    return Result.objects.filter(read__read_id = read_id, bitscore__gt = limit)

def create_json(ecnumber, limit):
    zero_nodes = get_ec_results(ecnumber, limit)
    get_children.depth_counter = 0
    
    json_file = open("/home/jjlaukka/Opiskelu/ohtuprojekti/Jit/Examples/RGraph/json_file.json", 'w')

    json_file.write("{\n")

    json_file.write("id: \"" + ecnumber + "\",\n")
    json_file.write("name: \"" + ecnumber + "\",\n")
    json_file.write("children: [" + getChildren(zero_nodes, "ec", limit) + "]\n")

    json_file.write("}")

def get_children(nodes, caller_id, limit):

    get_children.depth_counter += 1

    for obj in nodes:
        if caller_id == "ec":
            result = result + "\t{\n\tid: \"" + obj.db_entry.read_id + "\",\n"
            result = result + "\tname: \"" + obj.db_entry.read_id + "\",\n"
            result = result + "\tdata: {\n\t\trelation: \"<h4>relations here..</h4>\"\n\t},\n"

            if get_children.depth_counter < depth_limit:
                results = results + "\tchildren: ["
                children = get_db_result(obj.db_entry.read_id)
                results = results + get_children(children, "db", limit)

            else:
                results = results + "\tchildren: []\n\t}"
                get_children.depth_counter -= 1
                return results

        elif caller_id == "db":
            result = result + "\t{\n\tid: \"" + obj.read.read_id + "\",\n"
            result = result + "\tname: \"" + obj.read.read_id + "\",\n"
            result = result + "\tdata: {\n\t\trelation: \"<h4>relations here..</h4>\"\n\t},\n"
            results = results + "\tchildren: []\n\t}"
            get_children.depth_counter -= 1
            return results

#FOR NOW, LATER MAYBE EXTENDED TO ALLOW DEEPER GRAPHS..
#            if get_children.depth_counter < depth_limit:
#                results = results + "\tchildren: ["
#                children = get_rd_result(obj.read.read_id)
#                results = results + get_children(children, "rd", limit)
#
#            else:
#                results = results + "\tchildren: []\n\t}"
#                get_children.depth_counter -= 1
#                return results

    results = results +"]}\n"
    get_children.depth_counter -= 1
    return results


if __name__ == "__main__":
    create_json("1.2.3.22", 40)
