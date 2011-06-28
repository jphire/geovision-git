import json
import os
from geovision.viz.models import *
from geovision.settings import PROJECT_PATH

class NodeId:
	def __init__(self, id, type):
		self.id = id
		self.type = type

	def __repr__(self):
		return self.id

	def __hash__(self):
		return self.id.__hash__()
	
class QueryToJSON:
	"""
	Makes a query according to the parameters and generates graph JSON file
	from the fetched data.
	Nodes and edges are kept in a dictionary with node_ids as keys.
	Dictionary format is:
	{node_id : [node, {node_id : blast}]

	Currently assumes that both Read.read_id and DbEntry.db_id are foreign keys.
	"""
	def __init__(self, ec_number=None, db_entry=None, read=None,
				e_value_limit=1, bitscore_limit=0, depth_limit=2,
				max_amount=5):
		self.ec_number = ec_number
		self.db_entry = db_entry
		self.read = read
		self.e_value_limit = e_value_limit
		self.bitscore_limit = bitscore_limit
		self.depth_limit = depth_limit
		self.max_amount = max_amount
		self.nodes = {}
		if db_entry is None:
			if read is None:
				raise Exception("Either db_entry or read parameter must be supplied")
			else:
				self.startpoint = NodeId(read, "read")
		else:
			self.startpoint = NodeId(db_entry, "db_entry")
		self.startnode = self.get_node(self.startpoint)
		self.build_graph(self.startnode, self.depth_limit)

	def build_graph(self, startnode, maxdepth):
		self.nodes[self.get_node_id(startnode)] = (startnode, {})
		self.build_graph_level([startnode], 1, maxdepth)


	def build_graph_level(self, nodes, depth, maxdepth):
		if depth <= maxdepth:
			for node in nodes:
				queryset = self.make_blast_queryset(node)
				next_level_nodes = self.add_edges(node, queryset)
				self.build_graph_level(next_level_nodes, depth + 1, maxdepth)

	def make_blast_queryset(self, param = None):
		"""
		Function for making the blast table QuerySet. Takes only one parameter,
		an instance of DbEntry or Read object. Other query parameters are
		carried over as class parameters.

		Makes a QuerySet by stacking filters to an initial unfiltered QuerySet
		object. Returns an unevaluated QuerySet object, thus the actual db query
		is not made in this function.
		"""
		query = Blast.objects.all()
#		if self.ec_number is not None:
#			query = query.filter(ec_number = self.ec_number)
		if param.__class__ is DbEntry:
			query = query.filter(db_entry = param.db_id)
		elif param.__class__ is Read:
			query = query.filter(read = param.read_id)
		else:
			return None
		query = query.filter(error_value__lte = self.e_value_limit)
		query = query.filter(bitscore__gte = self.bitscore_limit)
		query = query.order_by('bitscore')
		return query[:self.max_amount]

	def add_edges(self, startnode, queryset):
		"""
		Adds (read/db id, Blast object) tuples to the set in index 1 in
		dict entry self.nodes[startnode id]. Queryset parameter is evaluated in
		this method.
		
		Returns set of next level nodes (Read or DbEntry objects) that have not
		been visited.
		"""
		next_level_nodes = set()
		if startnode.__class__ is DbEntry:
			for blast in queryset:
				readnode = blast.read
				readid = self.get_node_id(readnode)
				if readid not in self.nodes:
					self.nodes[readid] = (readnode, {})
					next_level_nodes.add(readnode)
				self.nodes[self.get_node_id(startnode)][1][readid] = blast
		elif startnode.__class__ is Read:
			for blast in queryset:
				dbnode = blast.db_entry
				db_id = self.get_node_id(dbnode)
				if db_id not in self.nodes:
					self.nodes[db_id] = (dbnode, {})
					next_level_nodes.add(dbnode)
				self.nodes[self.get_node_id(startnode)][1][db_id] = blast
		else:
			raise Exception("startnode class must be DbEntry or Read")
		return next_level_nodes

	def get_node(self, node_id):
		if node_id.type is "read":
			return Read.objects.get(read_id = node_id.id)
		elif node_id.type is "db_entry":
			return DbEntry.objects.get(db_id = node_id.id)
		else:
			raise Exception("Invalid node_id parameter, must be tuple (type, id)")

	def get_node_id(self, node):
		if node.__class__ is DbEntry:
			return NodeId(node.db_id, "db_entry")
		elif node.__class__ is Read:
			return NodeId(node.read_id, "read")
		else:
			raise Exception("Invalid node parameter, must be Read or DbEntry")

	def __repr__(self):
		return str(self.nodes)
			
#def graph_JSON(query_type, query_value, bitscorelimit, e_value_limit, depthlimit, max_amount):
#
#    ec_list = []
#    db_list = []
#    rd_list = []
#    depth_limit = depthlimit
#    result = ""
#    read_query = False
#    enzyme_query = False
#    db_query = False
#    json_file = open(PROJECT_PATH + "/static/json_test_file.js", 'w')
#
#    json_file.write("var json_data = ")
#
#    # read query
#    if query_type == 'read':
#        node_type = 'rd'
#        node = Read.objects.get(read_id=query_value)
#        root_nodes = get_rd_adjacents(query_value, bitscorelimit, max_amount, e_value_limit)
#
##    adjacents = json.dumps([(json.dumps({'nodeTo':node.db_entry, })) for node in root_nodes])
#    # s = json.dumps({'name':root_nodes.read, 'id':root_nodes.read, 'description':node.description, 'adjacents':adjacents})
#
#    adjacents = [({'nodeTo':obj.db_entry, 'data':{'$color':bitscore_to_hex(obj.bitscore)}}) for obj in root_nodes]
#    json.dump([{'name': "R1", 'id':"R12", 'description':node.description, 'adjacencies':adjacents}], json_file)
#    json_file.close()
#
#
#
#
#def bitscore_to_hex(bitscore):
#    if 0 < bitscore < 100:
#        return '#ff4444'
#
#    elif 100 <= bitscore < 500:
#        return '#aa5555'
#
#    else:
#        return '#ffffff'
#
#    #d = json.dump(d)
#
#
## returns Result objects that match the query arguments, used to get adjacencies to an entzyme class
## excludes nodes that are already visited
#
#def get_ec_adjacents(ecnumber, bitscorelimit, max_amount, e_value_limit):
#    res = DbUniprotEcs.objects.filter(ecs=ecnumber)
#    # ?? like this ??
#    return Blast.objects.filter(db_entry=res.db_entry, bitscore__gt=bitscorelimit, error_value__lt=e_value_limit).order_by('bitscore')[:max_amount].reverse()
#
## returns Result objects that match the query arguments, used to get adjacencies to a database entry
## excludes nodes that are already visited and below bitscorelimit. Return at most max_amount nodes
#
#def get_db_adjacents(db_entry_id, bitscorelimit, max_amount, e_value_limit, caller_type):
#    return Blast.objects.filter(db_entry=db_entry_id, bitscore__gt=bitscorelimit, error_value__lt=e_value_limit).order_by('bitscore')[:max_amount].reverse()
#
## returns Result objects that match the query arguments, used to get adjacencies to a read
## excludes nodes that are already visited
#
#def get_rd_adjacents(read_id, bitscorelimit, max_amount, e_value_limit):
#    return Result.objects.filter(read=read_id, bitscore__gt=bitscorelimit, error_value__lt=e_value_limit).order_by('bitscore')[:max_amount].reverse()
#
#if __name__ == "__main__":
#    print "Hello World"
