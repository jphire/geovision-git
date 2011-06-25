import os
import simplejson
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import *
from geovision.settings import PROJECTROOT


depth_limit = 0
json_file = open(PROJECTROOT + "/static/json_test_file.js", 'w')

# returns Result objects that match the query arguments, used to get adjacencies to an enzyme class
# excludes nodes that are already visited

def get_ec_adjacents(ecnumber, bitscorelimit, max_amount, e_value_limit):
	res = DbUniprotEcs.objects.filter(ecs = ecnumber)
	# ?? like this ??
	return Blast.objects.filter(db_entry = res.db_entry, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).order_by('bitscore')[:max_amount].reverse()

# returns Result objects that match the query arguments, used to get adjacencies to a database entry
# excludes nodes that are already visited and below bitscorelimit. Return at most max_amount nodes

def get_db_adjacents(db_entry_id, bitscorelimit, max_amount, e_value_limit):
	return Result.objects.filter(db_entry = db_entry_id, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).order_by('bitscore')[:max_amount].reverse()

# returns Result objects that match the query arguments, used to get adjacencies to a read
# excludes nodes that are already visited

def get_rd_adjacents(read_id, bitscorelimit, max_amount, e_value_limit):
	return Result.objects.filter(read = read_id, bitscore__gt = bitscorelimit, error_value__lt = e_value_limit).order_by('bitscore')[:max_amount].reverse()


def graph_JSON(query_type, query_value, bitscore_limit, e_value_limit, depthlimit, max_amount):

	global depth_limit
	global json_file
	depth_limit= depthlimit
	result = ""
	read_query = False
	enzyme_query = False
	db_query = False
	
	json_file.write("var json_data = ")
	get_edges.depth_counter = 0

	# read query
	if query_type == 'read':
		node = Read.objects.get(read_id = query_value)
		root_nodes = get_rd_adjacents(query_value, bitscore_limit, max_amount, e_value_limit)
		adjacents = [({'nodeTo':obj.db_entry, 'data':{'$color':bitscore_to_hex(obj.bitscore)}}) for obj in root_nodes]
		simplejson.dump([{'name': node.read_id, 'id':node.read_id, 'description':node.description, 'adjacencies':adjacents}], json_file)
		for node in root_nodes:
			get_edges(node, 'db', 'db', bitscore_limit, e_value_limit, max_amount)

	# enzyme query
	elif query_type == 'enzyme':
		node_type = 'ez'
		node = Read.objects.get(read_id = query_value)
		root_nodes = get_ec_adjacents(query_value, bitscore_limit, max_amount, e_value_limit)
		requested_type = 'db'

	# db query
	elif query_type == 'database':
		node = DbEntry.objects.get(db_id = query_value)
		root_nodes_1 = get_db_adjacents(query_value, bitscore_limit, max_amount, e_value_limit)
		#root_nodes_2 = get_db_adjacents(query_value, bitscorelimit, max_amount, e_value_limit)

		for node in root_nodes_1:
			get_edges(node, 'db', 'rd', bitscore_limit, e_value_limit, max_amount)
#		for node in root_nodes_2:
#			get_edges(node, node_type, requested_type, bitscore_limit, error_value_limit)

	
	json_file.close()

def get_edges(node, node_type, requested_type, bitscore_limit, e_value_limit, max_amount):
	global depth_limit
	global json_file
	get_edges.depth_counter += 1

	json_file.write("\n")

	if node_type == 'rd':
		read_node = Read.objects.get(read_id = node.read)
		edge_nodes = get_rd_adjacents(read_node.read_id, bitscore_limit, max_amount, e_value_limit)
		adjacents = [({'nodeTo':obj.db_entry, 'data':{'$color':bitscore_to_hex(obj.bitscore)}}) for obj in edge_nodes]
		simplejson.dump([{'name': node.read, 'id':node.read, 'description':read_node.description, 'adjacencies':adjacents}], json_file)

		if get_edges.depth_counter < depth_limit:
			for each_node in edge_nodes:
				get_edges(each_node, 'rd', 'db', bitscore_limit, e_value_limit, max_amount)

	elif node_type == 'ec':
		res = DbUniprotEcs.objects.filter(ecs = ecnumber)
		edge_nodes = get_ec_adjacents(ENZYMEVALUE, bitscore_limit, max_amount, e_value_limit)

	elif node_type == 'db':
		db_node = DbEntry.objects.get(db_id = node.db_entry)
		edge_nodes = get_db_adjacents(db_node.db_id, bitscore_limit, max_amount, e_value_limit)
		adjacents = [({'nodeTo':obj.read, 'data':{'$color':bitscore_to_hex(obj.bitscore)}}) for obj in edge_nodes]
		simplejson.dump([{'name': node.db_entry, 'id':node.db_entry, 'description':db_node.description, 'adjacencies':adjacents}], json_file)

		if get_edges.depth_counter < depth_limit:
			for each_node in edge_nodes:
				get_edges(each_node, 'db', 'rd', bitscore_limit, e_value_limit, max_amount)

		else:
			get_edges.depth_counter -= 1
			return

def bitscore_to_hex(bitscore):
	if 0 < bitscore < 100:
		return '#ff4444'

	elif 100 <= bitscore < 500:
		return '#aa5555'

	else:
		return '#ffffff'

	return

if __name__ == "__main__":
    print "Hello World"
