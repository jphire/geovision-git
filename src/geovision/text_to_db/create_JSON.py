import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import Blast, Read, DbEntry, Result
from geovision.settings import PROJECTROOT

# result is a string that contains the data that is to be written to json_file
result = ""

# the graph's depth limit from root node, defaults 3
depth_limit = 3

#to keep track of 'visited' nodes:
ec_list = []
db_list = []
rd_list = []


# THE DOUBLE UNDERSCORE CAN BE INEFFICIENT BECAUSE OF JOINS IN THE BACKGROUND: MAYBE HAVE TO BE CHANGED
# IN THE FUTURE!!!

# returns Result objects that match the query arguments, used to get adjancies to an entzyme class
# excludes nodes that are already visited
def get_ec_results(ecnumber, bitscorelimit, max_amount):
    global db_list
    return Result.objects.filter(ec_number = ecnumber, bitscore__gt = bitscorelimit).exclude(db_entry__read_id__in = db_list).order_by('bitscore').reverse()[:max_amount]

# returns Result objects that match the query arguments, used to get adjancies to a database entry
# excludes nodes that are already visited and below bitscorelimit. Return at most max_amount nodes
def get_db_results(db_entry_id, bitscorelimit, max_amount, caller_type):
    global ec_list, rd_list
    if caller_type == 'ec':
        return Result.objects.filter(db_entry__read_id = db_entry_id, bitscore__gt = bitscorelimit).exclude(ec_number__in = ec_list).order_by('bitscore').reverse()[:max_amount].distinct()

    elif caller_type == 'rd':
        return Result.objects.filter(db_entry__read_id = db_entry_id, bitscore__gt = bitscorelimit).exclude(read__read_id__in = rd_list).order_by('bitscore').reverse()[:max_amount].distinct()

# returns Result objects that match the query arguments, used to get adjancies to a read
# excludes nodes that are already visited
def get_rd_results(read_id, bitscorelimit, max_amount):
    global db_list
    return Result.objects.filter(read__read_id = read_id, bitscore__gt = bitscorelimit).exclude(db_entry__read_id__in = db_list).order_by('bitscore').reverse()[:max_amount].distinct()

# the main function that is called to create the json_file. If ecnumber is not 0, a query is made
# based on the given ecnumber. If ecnumber is 0, a query is made based on the read_id. bitscorelimit
# is used to cut off adjancies between nodes that are below this limit. depthlimit is used limit
# the depth of the graph. max_amount is upper limit for node's child amount.
def create_json(ecnumber, read_id, bitscorelimit, depthlimit, max_amount):

    # if read_id-based query
    if ecnumber == 0:
        root_nodes = get_rd_results(read_id, bitscorelimit, max_amount)
    # entzyme class query
    else:
        root_nodes = get_ec_results(ecnumber, bitscorelimit, max_amount)

    get_children.depth_counter = 0
    global depth_limit
    global ec_list, rd_list, db_list
    depth_limit = depthlimit

    json_file = open(PROJECTROOT + "/static/json_file.js", 'w')
    json_file.write("var json_data = {\n")

    json_file.write("id: \"" + ecnumber + "\",\n")
    json_file.write("name: \"" + ecnumber + "\",\n")

    json_file.write("data: [")
    # can be used to both entzyme- and read query:
    for node in root_nodes:
        json_file.write("{" + node.db_entry.read_id + ":\"" + node.db_entry.read_id + "\"}, ")
    
    json_file.write("],\n")
    json_file.write("children: [")

    if ecnumber == 0:
        for node in root_nodes:
            result = get_children(node, "rd", read_id, bitscorelimit, max_amount, 'ec')
    else:
        for node in root_nodes:
            result = get_children(node, "ec", ecnumber, bitscorelimit, max_amount, 'rd')

    json_file.write(result)
    json_file.write("]\n};")
    
    json_file.close()

# get_children is used to retrieve a node's adjancies to other nodes. node is the calling node,
# caller_class is the calling node's type(ec, db or rd), caller_id is the calling node's name or id,
# bitscorelimit and max_amount: see create_JSON(), db_child_type is used to get knowledge on which
# type of adjancies to a database node are requested(i.e. did we 'come' to database node from
# enzyme node or read node)
def get_children(node, caller_class, caller_id, bitscorelimit, max_amount, db_child_type):

    get_children.depth_counter += 1
    global result, db_list, rd_list, ec_list

    if caller_class == "ec" or caller_class == "rd":
        # add visited node to db_list:
        db_list.append(node.db_entry.read_id)
        result = result + "\t{\n\tid: \"" + node.db_entry.read_id + "\",\n"
        result = result + "\tname: \"" + node.db_entry.read_id + "\",\n"

        if caller_class == 'ec':
            children = get_db_results(node.db_entry.read_id, bitscorelimit, max_amount, 'rd')

        elif caller_class == 'rd':
            children = get_db_results(node.db_entry.read_id, bitscorelimit, max_amount, 'ec')

        result = result + "\tdata: [{parent: \"" + caller_id + "\"}, "

        if caller_class == 'ec':
            for child in children:
                result = result + "{" + child.read.read_id + ":\"" + child.read.read_id + "\"},"

        elif caller_class == 'rd':
            for child in children:
                result = result + "{\"" + child.ec_number + "\":\"" + child.ec_number + "\"},"

        #loose the last , ...
        result = result[:-1]
        result = result + "],\n"

        if get_children.depth_counter < depth_limit:
            result = result + "\tchildren: ["

            if caller_class == 'ec':
                for obj in children:
                    result = get_children(obj, "db", node.db_entry.read_id, bitscorelimit, max_amount, 'rd')

            elif caller_class == 'rd':
                for obj in children:
                    result = get_children(obj, "db", node.db_entry.read_id, bitscorelimit, max_amount, 'ec')

        else:
            result = result + "\tchildren: []\n\t},"
            get_children.depth_counter -= 1
            return result

    elif caller_class == "db":
        if db_child_type == 'rd':
            #we 'are' in read_id node, so add it to the visited list
            rd_list.append(node.read.read_id)
            result = result + "\t{\n\tid: \"" + node.read.read_id + "\",\n"
            result = result + "\tname: \"" + node.read.read_id + "\",\n"
            children = get_rd_results(node.read.read_id, bitscorelimit, max_amount)
        else:
            #we 'are' in enzyme node, so add it to the visited list
            ec_list.append(node.ec_number)
            result = result + "\t{\n\tid: \"" + node.ec_number + "\",\n"
            result = result + "\tname: \"" + node.ec_number + "\",\n"
            children = get_ec_results(node.ec_number, bitscorelimit, max_amount)

        result = result + "\tdata: [{parent: \"" + caller_id + "\"}, "
        for child in children:
            result = result + "{" + child.db_entry.read_id + ":\"" + child.db_entry.read_id + "\"},"
        #loose the last , ...
        result = result[:-1]
        result = result + "],\n"

        if get_children.depth_counter < depth_limit:
            result = result + "\tchildren: ["

            if db_child_type == 'rd':
                for child in children:
                    result = get_children(child, "rd", node.read.read_id, bitscorelimit, max_amount, '-')
            else:
                for child in children:
                    result = get_children(child, "ec", node.ec_number, bitscorelimit, max_amount, '-')

        else:
            result = result + "\tchildren: []\n\t},"
            get_children.depth_counter -= 1
            return result

    result = result +"]},\n"
    get_children.depth_counter -= 1
    return result

if __name__ == "__main__":
    create_json("1.2.3.22", 0, 40, 3, 200)
