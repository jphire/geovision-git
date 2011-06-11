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

#returns Result objects that match the query arguments, used to get adjancies to an entzyme class
def get_ec_results(ecnumber, bitscorelimit, max_amount):
    return Result.objects.filter(ec_number = ecnumber, bitscore__gt = bitscorelimit).order_by('bitscore').reverse()[:max_amount]

#returns Result objects that match the query arguments, used to get adjancies to a database entry
def get_db_results(db_entry_id, bitscorelimit, max_amount):
    return Result.objects.filter(db_entry__read_id = db_entry_id, bitscore__gt = bitscorelimit).order_by('bitscore').reverse()[:max_amount]

#returns Result objects that match the query arguments, used to get adjancies to a read
def get_rd_results(read_id, bitscorelimit, max_amount):
    return Result.objects.filter(read__read_id = read_id, bitscore__gt = bitscorelimit).order_by('bitscore').reverse()[:max_amount]

def create_json(ecnumber, read_id, bitscorelimit, depthlimit, max_amount):

    #if read-query
    if ecnumber == 0:
        root_nodes = get_rd_results(read_id, bitscorelimit, max_amount)
    #entzyme class query
    else:
        root_nodes = get_ec_results(ecnumber, bitscorelimit, max_amount)

    get_children.depth_counter = 0
    global depth_limit
    depth_limit = depthlimit

    json_file = open(PROJECTROOT + "/static/json_file.js", 'w')

    json_file.write("var json_data = {\n")

    json_file.write("id: \"" + ecnumber + "\",\n")
    json_file.write("name: \"" + ecnumber + "\",\n")

    json_file.write("data: [")

    #can be used to both entzyme- and read query:
    for child in root_nodes:
        json_file.write("{" + child.db_entry.read_id + ":\"" + child.db_entry.read_id + "\"}, ")
    
    json_file.write("],\n")

    json_file.write("children: [")

    if ecnumber == 0:
        for obj in root_nodes:
            result = get_children(obj, "rd", ecnumber, bitscorelimit, max_amount)
    else:
        for obj in root_nodes:
            result = get_children(obj, "ec", ecnumber, bitscorelimit, max_amount)

    json_file.write(result)
    json_file.write("]\n};")
    json_file.close()

def get_children(node, caller_class, caller_id, bitscorelimit, max_amount):

    get_children.depth_counter += 1
    global result

    if caller_class == "ec" or caller_class == 'rd':
        result = result + "\t{\n\tid: \"" + node.db_entry.read_id + "\",\n"
        result = result + "\tname: \"" + node.db_entry.read_id + "\",\n"
        children = get_db_results(node.db_entry.read_id, bitscorelimit, max_amount)

        result = result + "\tdata: [{parent: \"" + caller_id + "\"}, "
        for child in children:
            result = result + "{" + child.read.read_id + ":\"" + child.read.read_id + "\"},"
        #loose the last , ...
        result = result[:-1]
        result = result + "],\n"

        if get_children.depth_counter < depth_limit:
            result = result + "\tchildren: ["
            
            for obj in children:
                result = get_children(obj, "db", node.db_entry.read_id, bitscorelimit, max_amount)

        else:
            result = result + "\tchildren: []\n\t},"
            get_children.depth_counter -= 1
            return result

    elif caller_class == "db":
        result = result + "\t{\n\tid: \"" + node.read.read_id + "\",\n"
        result = result + "\tname: \"" + node.read.read_id + "\",\n"
        children = get_rd_results(node.read.read_id, bitscorelimit, max_amount)

        result = result + "\tdata: [{parent: \"" + caller_id + "\"}, "
        for child in children:
            result = result + "{" + child.db_entry.read_id + ":\"" + child.db_entry.read_id + "\"},"
        #loose the last , ...
        result = result[:-1]
        result = result + "],\n"

        if get_children.depth_counter < depth_limit:
            result = result + "\tchildren: ["

            for child in children:
                result = get_children(child, "rd", node.read.read_id, bitscorelimit, max_amount)

        else:
            result = result + "\tchildren: []\n\t},"
            get_children.depth_counter -= 1
            return result

    result = result +"]},\n"
    get_children.depth_counter -= 1
    return result

if __name__ == "__main__":
    create_json("1.2.3.22", 0, 40, 3, 200)
