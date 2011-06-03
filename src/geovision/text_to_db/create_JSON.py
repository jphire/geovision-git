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

def get_ec_results(ecnumber, limit):
    return Result.objects.filter(ec_number = ecnumber, bitscore__gt = limit)

def get_db_results(db_entry_id, limit):
    return Result.objects.filter(db_entry__read_id = db_entry_id, bitscore__gt = limit)

def get_rd_results(read_id, limit):
    return Result.objects.filter(read__read_id = read_id, bitscore__gt = limit)

def create_json(ecnumber, limit):
    zero_nodes = get_ec_results(ecnumber, limit)
    get_children.depth_counter = 0
    
    json_file = open(PROJECTROOT + "/static/json_file.json", 'w')

    json_file.write("{\n")

    json_file.write("id: \"" + ecnumber + "\",\n")
    json_file.write("name: \"" + ecnumber + "\",\n")
    json_file.write("children: [")
    for obj in zero_nodes:
        result = get_children(obj, "ec", limit)
    json_file.write(result)
    json_file.write("]\n")
    json_file.write("}")
    json_file.close()

def get_children(node, caller_id, limit):

    get_children.depth_counter += 1
    global result

    if caller_id == "ec":
        result = result + "\t{\n\tid: \"" + node.db_entry.read_id + "\",\n"
        result = result + "\tname: \"" + node.db_entry.read_id + "\",\n"
        result = result + "\tdata: {\n\t\trelation: \"<h4>relations here..</h4>\"\n\t},\n"

        if get_children.depth_counter < depth_limit:
            result = result + "\tchildren: ["
            children = get_db_results(node.db_entry.read_id, limit)
            for obj in children:
                result = get_children(obj, "db", limit)

        else:
            result = result + "\tchildren: []\n\t},"
            get_children.depth_counter -= 1
            return result

    elif caller_id == "db":
        result = result + "\t{\n\tid: \"" + node.read.read_id + "\",\n"
        result = result + "\tname: \"" + node.read.read_id + "\",\n"
        result = result + "\tdata: {\n\t\trelation: \"<h4>relations here..</h4>\"\n\t},\n"
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
    create_json("1.2.3.22", 40)
