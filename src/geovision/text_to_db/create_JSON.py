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


# returns Result objects that match the query arguments, used to get adjancies to an entzyme class
# excludes nodes that are already visited
def get_ec_results(ecnumber, bitscorelimit, max_amount, e_value_limit):
    global db_list
    return Result.objects.filter(ec_number = ecnumber, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).exclude(db_entry__db_id__in = db_list).order_by('bitscore').reverse()[:max_amount]

# returns Result objects that match the query arguments, used to get adjancies to a database entry
# excludes nodes that are already visited and below bitscorelimit. Return at most max_amount nodes
def get_db_results(db_entry_id, bitscorelimit, max_amount, e_value_limit, caller_type):
    global ec_list, rd_list
    if caller_type == 'rd':
        return Result.objects.filter(db_entry = db_entry_id, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).exclude(ec_number__in = ec_list).order_by('bitscore').reverse()[:max_amount]

    elif caller_type == 'ec':
        return Result.objects.filter(db_entry = db_entry_id, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).exclude(read__in = rd_list).order_by('bitscore').reverse()[:max_amount]

# returns Result objects that match the query arguments, used to get adjancies to a read
# excludes nodes that are already visited
def get_rd_results(read_id, bitscorelimit, max_amount, e_value_limit):
    global db_list
    return Result.objects.filter(read__read_id = read_id, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).exclude(db_entry__db_id__in = db_list).order_by('bitscore').reverse()[:max_amount]

# the main function that is called to create the json_file. If ecnumber is not 0, a query is made
# based on the given ecnumber. If ecnumber is 0, a query is made based on the read_id. bitscorelimit
# is used to cut off adjancies between nodes that are below this limit. depthlimit is used limit
# the depth of the graph. max_amount is upper limit for node's child amount.
def create_json(ecnumber, read_id, db_entry_id, bitscorelimit, e_value_limit, depthlimit, max_amount):

    result =""
    read_query = False
    enzyme_query = False
    db_query = False
    json_file = open(PROJECTROOT + "/static/json_file.js", 'w')

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
    # no valid query arguments given
    else:
        return 'error'

    get_children.depth_counter = 0
    global depth_limit
    global ec_list, rd_list, db_list
    depth_limit = depthlimit

    json_file.write("var json_data = {\n")

    if read_query:
        json_file.write("id: \"" + read_id + "\",\n")
        json_file.write("name: \"" + read_id + "\",\n")

    elif enzyme_query:
        json_file.write("id: \"" + ecnumber + "\",\n")
        json_file.write("name: \"" + ecnumber + "\",\n")

    elif db_query:
        json_file.write("id: \"" + db_entry_id + "\",\n")
        json_file.write("name: \"" + db_entry_id + "\",\n")

    json_file.write("data: { adjancies:\"")
    # dict is used to cut off multiple result lines that have the same db_entry
    dict = {}

    if enzyme_query or read_query:
        # can be used to both entzyme- and read query:
        for node in root_nodes:
            if node.db_entry.db_id not in dict:
                dict[node.db_entry.db_id] = 'db_entry';
                json_file.write(node.db_entry.db_id + ":</br>" + node.db_entry.description + "</br>")
    elif db_query:
        for node in root_nodes:
            if node.read.read_id not in dict:
                dict[node.read.read_id] = 'read';
                json_file.write(node.read.read_id + ": " + node.read.description + ", bitscore: " + str(node.bitscore) + "</br>")

        for node in root_nodes_2:
            if node.ec_number not in dict:
                dict[node.ec_number] = 'ec';
                json_file.write(node.ec_number + "</br>")

    json_file.write("\"},\n")
    json_file.write("children: [")

    dict = {}
    if read_query:
        rd_list.append(read_id)
        for node in root_nodes:
            if node.db_entry.db_id not in dict:
                dict[node.db_entry.db_id] = 'node.db_entry.db_id';
                result = get_children(node, "rd", read_id, bitscorelimit, max_amount, e_value_limit, 'ec')

    elif enzyme_query:
        ec_list.append(ecnumber)
        for node in root_nodes:
            if node.db_entry.db_id not in dict:
                dict[node.db_entry.db_id] = 'node.db_entry.db_id';
                result = get_children(node, "ec", ecnumber, bitscorelimit, max_amount, e_value_limit, 'rd')

    elif db_query:
        db_list.append(db_entry_id)
        for node in root_nodes:
            if node.read.read_id not in dict:
                dict[node.read.read_id] = 'node.read.read_id';
                result = get_children(node, "db", db_entry_id, bitscorelimit, max_amount, e_value_limit, 'rd')
        
        for node in root_nodes_2:
            if node.ec_number not in dict:
                dict[node.ec_number] = 'ec';
                result = get_children(node, "db", db_entry_id, bitscorelimit, max_amount, e_value_limit, 'ec')

    json_file.write(result)
    json_file.write("]\n};")
    
    json_file.close()

# get_children is used to retrieve a node's adjancies to other nodes. node is the calling node,
# caller_class is the calling node's type('ec' means enzyme, 'db' database and 'rd' read), caller_id is the calling node's name or id,
# bitscorelimit and max_amount: see create_JSON() comments, db_child_type is used to get knowledge on which
# type of adjancies to a database node are requested(i.e. did we 'come' to database node from
# enzyme node or read node)
def get_children(node, caller_class, caller_id, bitscorelimit, max_amount, e_value_limit, db_child_type):

    get_children.depth_counter += 1
    global result, db_list, rd_list, ec_list

    if caller_class == "ec" or caller_class == "rd":
        # add this node to visited nodes db_list:
        db_list.append(node.db_entry.db_id)
        result = result + "\t{\n\tid: \"" + node.db_entry.db_id + "\",\n"
        result = result + "\tname: \"" + node.db_entry.db_id + "\",\n"

        children_1 = get_db_results(node.db_entry.db_id, bitscorelimit, max_amount, e_value_limit, 'ec')
        children_2 = get_db_results(node.db_entry.db_id, bitscorelimit, max_amount, e_value_limit, 'rd')

        result = result + "\tdata: [{parent: \"" + caller_id + "\"}, "
        dict = {}
        # two sets of children for both read and enzyme adjancies
        for child in children_1:
            if child.read.read_id not in dict:
                dict[child.read.read_id] = 'child.read.read_id'
                result = result + "{" + child.read.read_id + ":\"" + child.read.read_id + "\"},"

        for child in children_2:
            if child.ec_number not in dict:
                dict[child.ec_number] = 'child.ec_number'
                result = result + "{\"" + child.ec_number + "\":\"" + child.ec_number + "\"},"
                    
        # drop the last ','
        result = result[:-1]
        result = result + "],\n"

        if get_children.depth_counter < depth_limit:
            dict = {}
            result = result + "\tchildren: ["

            for child in children_1:
                if child.read.read_id not in dict:
                    dict[child.read.read_id] = 'child.read.read_id'
                    result = get_children(child, "db", node.db_entry.db_id, bitscorelimit, max_amount, e_value_limit, 'rd')

            for child in children_2:
                if child.ec_number not in dict:
                    dict[child.ec_number] = 'child.ec_number'
                    result = get_children(child, "db", node.db_entry.db_id, bitscorelimit, max_amount, e_value_limit, 'ec')
                            
        else:
            result = result + "\tchildren: []\n\t},"
            get_children.depth_counter -= 1
            return result

    elif caller_class == "db":
        if db_child_type == 'rd':
            # we 'are' in read_id node, so add it to the visited list
            rd_list.append(node.read.read_id)
            result = result + "\t{\n\tid: \"" + node.read.read_id + "\",\n"
            result = result + "\tname: \"" + node.read.read_id + "\",\n"
            children = get_rd_results(node.read.read_id, bitscorelimit, max_amount, e_value_limit)
        else:
            # we 'are' in enzyme node, so add it to the visited list
            ec_list.append(node.ec_number)
            result = result + "\t{\n\tid: \"" + node.ec_number + "\",\n"
            result = result + "\tname: \"" + node.ec_number + "\",\n"
            children = get_ec_results(node.ec_number, bitscorelimit, max_amount, e_value_limit)

        result = result + "\tdata: [{parent: \"" + caller_id + "\"}, "
        dict = {}
        for child in children:
            if child.db_entry.db_id not in dict:
                dict[child.db_entry.db_id] = 'child.db_entry.db_id'
                result = result + "{" + child.db_entry.db_id + ":\"" + child.db_entry.db_id + "\"},"
        #loose the last , ...
        result = result[:-1]
        result = result + "],\n"

        if get_children.depth_counter < depth_limit:
            result = result + "\tchildren: ["
            dict = {}
            if db_child_type == 'rd':
                for child in children:
                    if child.db_entry.db_id not in dict:
                        dict[child.db_entry.db_id] = 'child.db_entry.db_id'
                        result = get_children(child, "rd", node.read.read_id, bitscorelimit, max_amount, e_value_limit, 'ec')
            else:
                for child in children:
                    if child.db_entry.db_id not in dict:
                        dict[child.db_entry.db_id] = 'child.db_entry.db_id'
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

    Read.objects.create(sample="SMPL1", read_id="R001", description="baz", data='ASD')
    Read.objects.create(sample="SMPL2", read_id="R002", description="baz", data='ASD')
    Read.objects.create(sample="SMPL3", read_id="R003", description="baz", data='ASD')
    Read.objects.create(sample="SMPL4", read_id="R004", description="baz", data='ASD')
    Read.objects.create(sample="SMPL3", read_id="R005", description="baz", data='ASD')
    Read.objects.create(sample="SMPL2", read_id="R006", description="baz", data='ASD')

    DbEntry.objects.create(source_file = "uniprot", db_id = "DB1", description="quux", data='ASD')
    DbEntry.objects.create(source_file = "uniprot", db_id = "DB2", description="quux", data='ASD')
    DbEntry.objects.create(source_file = "uniprot", db_id = "DB3", description="quux", data='ASD')
    DbEntry.objects.create(source_file = "uniprot", db_id = "DB4", description="quux", data='ASD')
    DbEntry.objects.create(source_file = "uniprot", db_id = "DB5", description="quux", data='ASD')
    DbEntry.objects.create(source_file = "uniprot", db_id = "DB6", description="quux", data='ASD')
    DbEntry.objects.create(source_file = "uniprot", db_id = "DB7", description="quux", data='ASD')

    read1 = Read.objects.get(read_id="R001")
    read2 = Read.objects.get(read_id="R002")
    read3 = Read.objects.get(read_id="R003")
    read4 = Read.objects.get(read_id="R004")
    read5 = Read.objects.get(read_id="R005")
    read6 = Read.objects.get(read_id="R006")

    db_entry1= DbEntry.objects.get(db_id="DB1")
    db_entry2= DbEntry.objects.get(db_id="DB2")
    db_entry3= DbEntry.objects.get(db_id="DB3")
    db_entry4= DbEntry.objects.get(db_id="DB4")
    db_entry5= DbEntry.objects.get(db_id="DB5")
    db_entry6= DbEntry.objects.get(db_id="DB6")
    db_entry7= DbEntry.objects.get(db_id="DB7")

    Result.objects.create(read=read1, db_entry=db_entry1, evident_type="l", ec_number="1.1.2.22",
                    error_value=0.005, bitscore=50)
    Result.objects.create(read=read2, db_entry=db_entry1, evident_type="l", ec_number="1.1.2.22",
                    error_value=0.002, bitscore=30)
    Result.objects.create(read=read3, db_entry=db_entry2, evident_type="l", ec_number="1.1.2.22",
                    error_value=0.005, bitscore=50)
    Result.objects.create(read=read5, db_entry=db_entry4, evident_type="l", ec_number="1.1.2.24",
                    error_value=0.002, bitscore=30)
    Result.objects.create(read=read4, db_entry=db_entry6, evident_type="l", ec_number="1.1.2.22",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read=read1, db_entry=db_entry2, evident_type="l", ec_number="1.1.2.22",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read=read1, db_entry=db_entry2, evident_type="l", ec_number="1.1.2.24",
                    error_value=0.004, bitscore=50)
    Result.objects.create(read=read1, db_entry=db_entry3, evident_type="l", ec_number="1.1.2.23",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read=read2, db_entry=db_entry5, evident_type="l", ec_number="1.1.2.24",
                    error_value=0.001, bitscore=50)


    Result.objects.create(read=read4, db_entry=db_entry6, evident_type="l", ec_number="1.1.2.22",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read=read1, db_entry=db_entry2, evident_type="l", ec_number="1.1.2.22",
                    error_value=0.003, bitscore=50)
    Result.objects.create(read=read1, db_entry=db_entry2, evident_type="l", ec_number="1.1.2.24",
                    error_value=0.002, bitscore=50)
    Result.objects.create(read=read1, db_entry=db_entry3, evident_type="l", ec_number="1.1.2.23",
                    error_value=0.003, bitscore=50)
    Result.objects.create(read=read2, db_entry=db_entry4, evident_type="l", ec_number="1.1.2.24",
                    error_value=0.002, bitscore=50)

if __name__ == "__main__":
    create_json(0, 0, "DB1", 20, 0.001, 3, 200)
