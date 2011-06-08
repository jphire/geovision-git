# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jjlaukka"
__date__ ="$Jun 1, 2011 1:56:40 PM$"

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import Blast, Read, DbEntry, Result
from geovision.settings import PROJECTROOT

result = ""
depth_limit = 3

#THE DOUBLE UNDERSCORE CAN BE INEFFICIENT BECAUSE OF JOINS IN THE BACKGROUND: MAYBE HAVE TO BE CHANGED
#IN THE FUTURE!!!

def get_ec_results(ecnumber, bitscorelimit):
    return Result.objects.filter(ec_number = ecnumber, bitscore__gt = bitscorelimit)

def get_db_results(db_entry_id, bitscorelimit):
    return Result.objects.filter(db_entry__read_id = db_entry_id, bitscore__gt = bitscorelimit)

def get_rd_results(read_id, bitscorelimit):
    return Result.objects.filter(read__read_id = read_id, bitscore__gt = bitscorelimit)

def create_json(ecnumber, bitscorelimit, depthlimit):

    zero_nodes = get_ec_results(ecnumber, bitscorelimit)
    get_children.depth_counter = 0
    global depth_limit
    depth_limit = depthlimit

    json_file = open(PROJECTROOT + "/static/json_file.js", 'w')

    json_file.write("var json_data = {\n")

    json_file.write("id: \"" + ecnumber + "\",\n")
    json_file.write("name: \"" + ecnumber + "\",\n")

    json_file.write("data: [")
    for child in zero_nodes:
        json_file.write("{" + child.db_entry.read_id + ":\"" + child.db_entry.read_id + "\"}, ")
    json_file.write("],\n")

    json_file.write("children: [")
    for obj in zero_nodes:
        result = get_children(obj, "ec", ecnumber, bitscorelimit)
    json_file.write(result)
    json_file.write("]\n};")
    json_file.close()

def get_children(node, caller_class, caller_id, bitscorelimit):

    get_children.depth_counter += 1
    global result

    if caller_class == "ec":
        result = result + "\t{\n\tid: \"" + node.db_entry.read_id + "\",\n"
        result = result + "\tname: \"" + node.db_entry.read_id + "\",\n"
        children = get_db_results(node.db_entry.read_id, bitscorelimit)

        result = result + "\tdata: [{parent: \"" + caller_id + "\"}, "
        for child in children:
            result = result + "{" + child.read.read_id + ":\"" + child.read.read_id + "\"},"
        #lose the last , ...
        result = result[:-1]
        result = result + "],\n"

        if get_children.depth_counter < depth_limit:
            result = result + "\tchildren: ["
            
            for obj in children:
                result = get_children(obj, "db", node.db_entry.read_id, bitscorelimit)

        else:
            result = result + "\tchildren: []\n\t},"
            get_children.depth_counter -= 1
            return result

    elif caller_class == "db":
        result = result + "\t{\n\tid: \"" + node.read.read_id + "\",\n"
        result = result + "\tname: \"" + node.read.read_id + "\",\n"
        result = result + "\tdata: {\n\t\tparent: \"" + caller_id + "\"\n\t},\n"
        result = result + "\tchildren: []\n\t}"
        result = result + ",\n"
        get_children.depth_counter -= 1
        return result

#FOR NOW, LATER MAYBE EXTENDED TO ALLOW DEEPER GRAPHS..
#            if get_children.depth_counter < depth_limit:
#                result = result + "\tchildren: ["
#                children = get_rd_result(obj.read.read_id)
#                result = result + get_children(children, "rd", limit)
#
#            else:
#                result = result + "\tchildren: []\n\t}"
#                get_children.depth_counter -= 1
#                return result

    result = result +"]},\n"
    get_children.depth_counter -= 1
    return result

if __name__ == "__main__":
    create_json("1.2.3.22", 40, 3)
