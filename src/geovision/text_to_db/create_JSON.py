import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import Blast, Read, DbEntry, Result
from geovision.settings import PROJECTROOT

# result is a string that contains the data that is to be written to json_file
result = ""

# the graph's depth limit from root node, defaults 3
depth_limit = 3

# to keep track of 'visited' nodes:
ec_list = []
db_list = []
rd_list = []

# THE DOUBLE UNDERSCORE CAN BE INEFFICIENT BECAUSE OF JOINS IN THE BACKGROUND: MAYBE HAVE TO BE CHANGED
# IN THE FUTURE!!


# returns Result objects that match the query arguments, used to get adjacencies to an entzyme class
# excludes nodes that are already visited
def get_ec_results(ecnumber, bitscorelimit, max_amount, e_value_limit):
    global db_list
    return Result.objects.filter(ec_number = ecnumber).exclude(db_entry__in = db_list).order_by('bitscore')[:max_amount].reverse()

# returns Result objects that match the query arguments, used to get adjacencies to a database entry
# excludes nodes that are already visited and below bitscorelimit. Return at most max_amount nodes
def get_db_results(db_entry_id, bitscorelimit, max_amount, e_value_limit, caller_type):
    global ec_list, rd_list
    if caller_type == 'rd':
        return Result.objects.filter(db_entry = db_entry_id).exclude(ec_number__in = ec_list).order_by('bitscore')[:max_amount].reverse()

    elif caller_type == 'ec':
        return Result.objects.filter(db_entry = db_entry_id).exclude(read__in = rd_list).order_by('bitscore')[:max_amount].reverse()

# returns Result objects that match the query arguments, used to get adjacencies to a read
# excludes nodes that are already visited
def get_rd_results(read_id, bitscorelimit, max_amount, e_value_limit):
    global db_list
    return Result.objects.filter(read = read_id).exclude(db_entry__in = db_list).order_by('bitscore')[:max_amount].reverse()

# the main function that is called to create the json_file. If ecnumber is not 0, a query is made
# based on the given ecnumber. If ecnumber is 0, a query is made based on the read_id. bitscorelimit
# is used to cut off adjacencies between nodes that are below this limit. depthlimit is used limit
# the depth of the graph. max_amount is upper limit for node's child amount.
def create_json(ecnumber, read_id, db_entry_id, bitscorelimit, e_value_limit, depthlimit, max_amount):

    global ec_list, rd_list, db_list
    global depth_limit
    global result
    ec_list = []
    db_list = []
    rd_list = []
    depth_limit = depthlimit
    result = ""
    read_query = False
    enzyme_query = False
    db_query = False
    json_file = open(PROJECTROOT + "/static/json_file.js", 'w')

    json_file.write("var json_data = {\n")

    if depth_limit == 0:
        return 'error_no_children'
    
    # read query
    if ecnumber == 0 and db_entry_id == 0:
        read_query = True
        root_nodes = get_rd_results(read_id, bitscorelimit, max_amount, e_value_limit)
    # entzyme query
    elif read_id == 0 and db_entry_id == 0:
        enzyme_query = True
        root_nodes = get_ec_results(ecnumber, bitscorelimit, max_amount, e_value_limit)
    # database entry query
    elif ecnumber == 0 and read_id == 0:
        db_query = True
        # two query sets are needed to get both enzyme- and read result nodes for a db node
        root_nodes = get_db_results(db_entry_id, bitscorelimit, max_amount, e_value_limit, 'ec')
        root_nodes_2 = get_db_results(db_entry_id, bitscorelimit, max_amount, e_value_limit, 'rd')
        if root_nodes == [] or root_nodes_2 == []:
            return 'error_no_children'

    # no valid query arguments given
    else:
        return 'error_no_query'
    
    if root_nodes == []:
        return 'error_no_children'

    if read_query:
        json_file.write("id: \"" + read_id + "\",\n")
        json_file.write("name: \"" + read_id + "\",\n")

    elif enzyme_query:
        json_file.write("id: \"" + ecnumber + "\",\n")
        json_file.write("name: \"" + ecnumber + "\",\n")

    elif db_query:
        json_file.write("id: \"" + db_entry_id + "\",\n")
        json_file.write("name: \"" + db_entry_id + "\",\n")

    json_file.write("data: { adjacencies:\"")

    get_children.depth_counter = 0

    # dict is used to cut off multiple result lines that have the same db_entry
    dict = {}

    if enzyme_query or read_query:
        # can be used to both entzyme- and read query:
        for node in root_nodes:
            if node.db_entry not in dict:
                dict[node.db_entry] = 'db_entry';
                if enzyme_query:
                    json_file.write("DB entry: '" + node.db_entry + "'</br>")# TODO: db_entry's description
                elif read_query:
                    json_file.write("DB entry: '" + node.db_entry + "', bitscore: " + str(node.bitscore) + "</br>") # TODO: db_entry's description
    elif db_query:
        for node in root_nodes:
            if node.read not in dict:
                dict[node.read] = 'read';
                json_file.write("Read: '" + node.read + "', bitscore: " + str(node.bitscore) + "</br>")

        for node in root_nodes_2:
            if node.ec_number not in dict:
                dict[node.ec_number] = 'ec';
                json_file.write("Enzyme: '" + node.ec_number + "'</br>")

    json_file.write("\"},\n")
    json_file.write("children: [")

    dict = {}
    if read_query:
        rd_list.append(read_id)
        for node in root_nodes:
            if node.db_entry not in dict:
                dict[node.db_entry] = 'node.db_entry';
                result = get_children(node, "rd", read_id, bitscorelimit, max_amount, e_value_limit, 'ec')

    elif enzyme_query:
        ec_list.append(ecnumber)
        for node in root_nodes:
            if node.db_entry not in dict:
                dict[node.db_entry] = 'node.db_entry';
                result = get_children(node, "ec", ecnumber, bitscorelimit, max_amount, e_value_limit, 'rd')

    elif db_query:
        db_list.append(db_entry_id)
        for node in root_nodes:
            if node.read not in dict:
                dict[node.read] = 'node.read';
                result = get_children(node, "db", db_entry_id, bitscorelimit, max_amount, e_value_limit, 'rd')
        
        for node in root_nodes_2:
            if node.ec_number not in dict:
                dict[node.ec_number] = 'ec';
                result = get_children(node, "db", db_entry_id, bitscorelimit, max_amount, e_value_limit, 'ec')

    json_file.write(result)
    json_file.write("]\n};")
    
    json_file.close()

# get_children is used to retrieve a node's adjacencies to other nodes. node is the calling node,
# caller_class is the calling node's type('ec' means enzyme, 'db' database and 'rd' read), caller_id is the calling node's name or id,
# bitscorelimit and max_amount: see create_JSON() comments, db_child_type is used to get knowledge on which
# type of adjacencies to a database node are requested(i.e. did we 'come' to database node from
# enzyme node or read node)
def get_children(node, caller_class, caller_id, bitscorelimit, max_amount, e_value_limit, db_child_type):

    get_children.depth_counter += 1
    global result, db_list, rd_list, ec_list

    if caller_class == "ec" or caller_class == "rd":
        # add this node to visited nodes db_list:
        db_list.append(node.db_entry)
        result = result + "\t{\n\tid: \"" + node.db_entry + "\",\n"
        result = result + "\tname: \"" + node.db_entry + "\",\n"

        if get_children.depth_counter < depth_limit:
            children_1 = get_db_results(node.db_entry, bitscorelimit, max_amount, e_value_limit, 'ec')
            children_2 = get_db_results(node.db_entry, bitscorelimit, max_amount, e_value_limit, 'rd')
        else:
            children_1 = []
            children_2 = []

        if caller_class == "ec":
            result = result + "\tdata: {parent: \"Enzyme: '" + caller_id + "'</br>\", "
        elif caller_class == "rd":
            result = result + "\tdata: {parent: \"Read: '" + caller_id + "', bitscore: " + str(node.bitscore) + "</br>\", "
        dict = {}
        # two sets of children for both read and enzyme adjacencies
        result = result + "reads: \""
        for child in children_1:
            if child.read not in dict:
                dict[child.read] = 'child.read'
                result = result + "Read: '" + child.read + "', bitscore: " + str(node.bitscore) + "</br>"

        result = result + "\", enzymes: \""

        for child in children_2:
            if child.ec_number not in dict:
                dict[child.ec_number] = 'child.ec_number'
                result = result + "Enzyme: '" + child.ec_number + "'<br>"

        result = result + "\"}"
        result = result + ",\n"

        if get_children.depth_counter < depth_limit:
            dict = {}
            result = result + "\tchildren: ["

            for child in children_1:
                if child.read not in dict:
                    dict[child.read] = 'child.read'
                    result = get_children(child, "db", node.db_entry, bitscorelimit, max_amount, e_value_limit, 'rd')

            for child in children_2:
                if child.ec_number not in dict:
                    dict[child.ec_number] = 'child.ec_number'
                    result = get_children(child, "db", node.db_entry, bitscorelimit, max_amount, e_value_limit, 'ec')
                            
        else:
            result = result + "\tchildren: []\n\t},"
            get_children.depth_counter -= 1
            return result

    elif caller_class == "db":
        if db_child_type == 'rd':
            # we 'are' in read_id node, so add it to the visited list
            rd_list.append(node.read)
            result = result + "\t{\n\tid: \"" + node.read + "\",\n"
            result = result + "\tname: \"" + node.read + "\",\n"

            if get_children.depth_counter < depth_limit:
                children = get_rd_results(node.read, bitscorelimit, max_amount, e_value_limit)
            else:
                children = []
        else:
            # we 'are' in enzyme node, so add it to the visited list
            ec_list.append(node.ec_number)
            result = result + "\t{\n\tid: \"" + node.ec_number + "\",\n"
            result = result + "\tname: \"" + node.ec_number + "\",\n"
            children = get_ec_results(node.ec_number, bitscorelimit, max_amount, e_value_limit)
        if db_child_type == 'ec':
            result = result + "\tdata: {parent: \"DB entry: '" + caller_id + "'</br>\", dbentrys: \""
        
        elif db_child_type == 'rd':
            result = result + "\tdata: {parent: \"DB entry: '" + caller_id + "', bitscore: " + str(node.bitscore) + "</br>\", dbentrys: \""

        dict = {}
        for child in children:
            if child.db_entry not in dict:
                dict[child.db_entry] = 'child.db_entry'
                result = result + "DB entry: '" + child.db_entry + "'</br>"
        #loose the last , ...
        result = result + "\"}"
        # result = result[:-1]
        result = result + ",\n"

        if get_children.depth_counter < depth_limit:
            result = result + "\tchildren: ["
            dict = {}
            if db_child_type == 'rd':
                for child in children:
                    if child.db_entry not in dict:
                        dict[child.db_entry] = 'child.db_entry'
                        result = get_children(child, "rd", node.read, bitscorelimit, max_amount, e_value_limit, 'ec')
            else:
                for child in children:
                    if child.db_entry not in dict:
                        dict[child.db_entry] = 'child.db_entry'
                        result = get_children(child, "ec", node.ec_number, bitscorelimit, max_amount, e_value_limit, 'rd')

        else:
            result = result + "\tchildren: []\n\t},"
            get_children.depth_counter -= 1
            return result

    result = result +"]},\n"
    get_children.depth_counter -= 1
    return result

def setupderp():

    Read.objects.filter(data='ASD').delete()
    DbEntry.objects.filter(data='ASD').delete()
    Result.objects.filter(evident_type='l').delete()

    Result.objects.create(read="R1", db_entry="DB1", evident_type="l", ec_number="1.1.2.22",
                    error_value=0.005, bitscore=50)
    Result.objects.create(read="R2", db_entry="DB1", evident_type="l", ec_number="1.1.2.22",
                    error_value=0.002, bitscore=30)
    Result.objects.create(read="R3", db_entry="DB2", evident_type="l", ec_number="1.1.2.22",
                    error_value=0.005, bitscore=50)
    Result.objects.create(read="R5", db_entry="DB4", evident_type="l", ec_number="1.1.2.24",
                    error_value=0.002, bitscore=30)
    Result.objects.create(read="R4", db_entry="DB6", evident_type="l", ec_number="1.1.2.22",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read="R1", db_entry="DB2", evident_type="l", ec_number="1.1.2.22",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read="R1", db_entry="DB2", evident_type="l", ec_number="1.1.2.24",
                    error_value=0.004, bitscore=50)
    Result.objects.create(read="R1", db_entry="DB3", evident_type="l", ec_number="1.1.2.23",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read="R2", db_entry="DB5", evident_type="l", ec_number="1.1.2.24",
                    error_value=0.001, bitscore=50)


    Result.objects.create(read="R4", db_entry="DB6", evident_type="l", ec_number="1.1.2.22",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read="R1", db_entry="DB2", evident_type="l", ec_number="1.1.2.22",
                    error_value=0.003, bitscore=50)
    Result.objects.create(read="R1", db_entry="DB2", evident_type="l", ec_number="1.1.2.24",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read="R1", db_entry="DB3", evident_type="l", ec_number="1.1.2.23",
                    error_value=0.003, bitscore=50)
    Result.objects.create(read="R1", db_entry="DB4", evident_type="l", ec_number="1.1.2.24",
                    error_value=0.002, bitscore=50)


if __name__ == "__main__":
    create_json(0, 0, "DB1", 20, 0.001, 3, 200)
