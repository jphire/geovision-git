import os
import simplejson
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import *
from geovision.settings import PROJECTROOT

def graph_JSON(query_type, query_value, bitscorelimit, e_value_limit, depthlimit, max_amount):

    ec_list = []
    db_list = []
    rd_list = []
    depth_limit = depthlimit
    result = ""
    read_query = False
    enzyme_query = False
    db_query = False
    json_file = open(PROJECTROOT + "/static/json_test_file.js", 'w')

    json_file.write("var json_data = ")

    # read query
    if query_type == 'read':
        node_type = 'rd'
        node = Read.objects.get(read_id = query_value)
        root_nodes = get_rd_adjacents(query_value, bitscorelimit, max_amount, e_value_limit)

#    adjacents = simplejson.dumps([(simplejson.dumps({'nodeTo':node.db_entry, })) for node in root_nodes])
    # s = simplejson.dumps({'name':root_nodes.read, 'id':root_nodes.read, 'description':node.description, 'adjacents':adjacents})

    adjacents = simplejson.dumps([(simplejson.dumps({'nodeTo':obj.db_entry, 'data':simplejson.dumps({'$color':bitscore_to_hex(obj.bitscore)})})) for obj in root_nodes])

    simplejson.dump({'name': "R1", 'id':"R1", 'description':node.description, 'adjacents':adjacents}, json_file)
    json_file.close()

    


def bitscore_to_hex(bitscore):
    if 0 < bitscore < 100:
        return '#ff4444'
    
    elif 100 <= bitscore < 500:
        return '#aa5555'

    else:
        return '#ffffff'

    #d = simplejson.dump(d)


# returns Result objects that match the query arguments, used to get adjacencies to an entzyme class
# excludes nodes that are already visited

def get_ec_adjacents(ecnumber, bitscorelimit, max_amount, e_value_limit):
    res = DbUniprotEcs.objects.filter(ecs = ecnumber)
    # ?? like this ??
    return Blast.objects.filter(db_entry = res.db_entry, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).order_by('bitscore')[:max_amount].reverse()

# returns Result objects that match the query arguments, used to get adjacencies to a database entry
# excludes nodes that are already visited and below bitscorelimit. Return at most max_amount nodes

def get_db_adjacents(db_entry_id, bitscorelimit, max_amount, e_value_limit, caller_type):
    return Blast.objects.filter(db_entry = db_entry_id, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).order_by('bitscore')[:max_amount].reverse()

# returns Result objects that match the query arguments, used to get adjacencies to a read
# excludes nodes that are already visited

def get_rd_adjacents(read_id, bitscorelimit, max_amount, e_value_limit):
    return Result.objects.filter(read = read_id, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).order_by('bitscore')[:max_amount].reverse()

if __name__ == "__main__":
    print "Hello World"
