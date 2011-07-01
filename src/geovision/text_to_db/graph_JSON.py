import json
from geovision.viz.models import *

class NodeEdgeJSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, Node) or isinstance(o, Edge):
			return o.dict
		return json.JSONEncoder.default(self, o)

class Node:
	def __init__(self, dataobject):
		self.dict = {}
		if isinstance(dataobject, DbEntry):
			self.type = "db_entry"
			self.dict["id"] = dataobject.db_id
			self.dict["name"] = dataobject.db_id
			self.dict["data"] = {}
			self.dict["data"]["source"] = dataobject.source_file
			self.dict["data"]["description"] = dataobject.description
			if dataobject.source_file == "uniprot":
				self.dict["data"]["sub_db"] = dataobject.sub_db
				self.dict["data"]["entry_name"] = dataobject.entry_name
				self.dict["data"]["os_field"] = dataobject.os_field
				self.dict["data"]["other_info"] = dataobject.other_info
				self.dict["data"]["type"] = "dbentry"
		elif isinstance(dataobject, Read):
			self.type = "read"
			self.dict["id"] = dataobject.read_id
			self.dict["name"] = dataobject.read_id
			self.dict["data"] = {}
			self.dict["data"]["description"] = dataobject.description
			self.dict["data"]["type"] = "read"
		else:
			raise Exception("parameter class must be Read or DbEntry")
		self.dict["adjacencies"] = []


	def __repr__(self):
		return json.dumps(self.dict, cls=NodeEdgeJSONEncoder)

	def __hash__(self):
		return self.dict["id"].__hash__()

	def __eq__(self, other):
		if isinstance(other, Node):
			return ((self.type == other.type) and (self.dict["id"] == other.dict["id"]))
		else:
			return False

class Edge:
	def __init__(self, nodeTo, blastobject):
		if nodeTo is None:
			raise Exception("Must supply nodeTo parameter")
		if not isinstance(blastobject, Blast):
			raise Exception("Second parameter must be a blast object, is " + str(blastobject.__class__))
		self.dict = {}
		self.dict["nodeTo"] = nodeTo
		self.dict["data"] = {}
		self.dict["data"]["read"] = blastobject.read.read_id
		self.dict["data"]["database_name"] = blastobject.database_name
		self.dict["data"]["db_entry"] = blastobject.db_entry.db_id
		self.dict["data"]["length"] = blastobject.length
#		self.dict["data"]["pident"] = blastobject.pident
#		self.dict["data"]["mismatch"] = blastobject.mismatch
#		self.dict["data"]["gapopen"] = blastobject.gapopen
#		self.dict["data"]["qstart"] = blastobject.qstart
#		self.dict["data"]["qend"] = blastobject.qend
#		self.dict["data"]["sstart"] = blastobject.sstart
#		self.dict["data"]["send"] = blastobject.send
		self.dict["data"]["error_value"] = blastobject.error_value
		self.dict["data"]["bitscore"] = blastobject.bitscore
############## Graph visualization style options below ################
		self.dict["data"]["$color"] = bitscore_to_hex(blastobject.bitscore)
		self.dict["data"]["$type"] = "arrow"
		self.dict["data"]["$dim"] = 15
		self.dict["data"]["$lineWidth"] = 5
		self.dict["data"]["$alpha"] = 1
		self.dict["data"]["$epsilon"] = 7

	def __repr__(self):
		return json.dumps(self.dict, cls=NodeEdgeJSONEncoder)

	def __eq__(self, other):
		if isinstance(other, Edge):
			return ((self.nodeTo == other.nodeTo)
					and (self.dict["data"]["read"] == other.dict["data"]["read"])
					and (self.dict["data"]["db_entry"] == other.dict["data"]["db_entry"]))
		else:
			return False

class NodeId:
	"""
	NodeId class used as a node_id keys in node dictionary. It is simply
	a container for type information.
	"""
	def __init__(self, id, type):
		self.id = id
		self.type = type

	def __repr__(self):
		return self.id

	def __hash__(self):
		return self.id.__hash__()

	def __eq__(self, other):
		if isinstance(other, NodeId):
			return (self.id == other.id) and (self.type == other.type)
		else:
			return False
	
class QueryToJSON:
	"""
	Makes a query according to the parameters and generates graph JSON file
	from the fetched data.

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
		self.nodes = []
		if db_entry is None:
			if read is None:
				raise Exception("Either db_entry or read parameter must be supplied")
			else:
				self.startpoint = NodeId(read, "read")
		else:
			if read is not None:
				raise Exception("Cannot use both read and db_entry as starting point")
			self.startpoint = NodeId(db_entry, "db_entry")
		self.startnode = self.get_node(self.startpoint)
		self.build_graph(self.startnode, self.depth_limit)

	def build_graph(self, startnode, maxdepth):
		self.nodes.append(startnode)
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
		an instance of Node object. Other query parameters are
		carried over as class parameters.

		Makes a QuerySet by stacking filters to an initial unfiltered QuerySet
		object. Returns an unevaluated QuerySet object, thus the actual db query
		is not made in this function.
		"""
		query = Blast.objects.all()
#		if self.ec_number is not None:
#			query = query.filter(ec_number = self.ec_number)
		if param.type == "db_entry":
			query = query.filter(db_entry = param.dict["id"])
		elif param.type == "read":
			query = query.filter(read = param.dict["id"])
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
		if startnode.type == "db_entry":
			for blast in queryset:
				readnode = Node(blast.read)
				readid = self.get_node_id(readnode)
				if readnode not in self.nodes:
					self.nodes.append(readnode)
					next_level_nodes.add(readnode)
				startnode.dict["adjacencies"].append(Edge(readid.id, blast))
		elif startnode.type is "read":
			for blast in queryset:
				dbnode = Node(blast.db_entry)
				db_id = self.get_node_id(dbnode)
				if dbnode not in self.nodes:
					self.nodes.append(dbnode)
					next_level_nodes.add(dbnode)
				startnode.dict["adjacencies"].append(Edge(db_id.id, blast))
		else:
			raise Exception("startnode type must be db_entry or read")
		return next_level_nodes

	def get_node(self, node_id):
		if node_id.type is "read":
			return Node(Read.objects.get(read_id = node_id.id))
		elif node_id.type is "db_entry":
			return Node(DbEntry.objects.get(db_id = node_id.id))
		else:
			raise Exception("Invalid node_id parameter, must be tuple (type, id)")

	def get_node_id(self, node):
		if node.type == "db_entry":
			return NodeId(node.dict["id"], "db_entry")
		elif node.type == "read":
			return NodeId(node.dict["id"], "read")
		else:
			raise Exception("Invalid node parameter, must be Node of type read or db_entry")

	def dump_to_json(self):
		return str(self.nodes)

	def write_to_json(self, file="/static/json_test_file.js"):
		json_file = None
		try:
			json_file = open(PROJECTROOT + file, 'w')
		except NameError:
			json_file = open(file, 'w')
		json_file.write(str(self.nodes))
#		json_file.write(json.dumps(self.nodes)) # what???
		json_file.close()
		
	def __repr__(self):
		return str(self.nodes)

def bitscore_to_hex(bitscore):
	if 0 < bitscore < 10:
		return '#C0C0C0'

	elif 10 <= bitscore < 20:
		return '#FFFF00'

	elif 20 <= bitscore < 30:
		return '#0000FF'

	elif 30 <= bitscore:
		return '#00FF00'

	else:
		return '#CCCCCC'
			
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
