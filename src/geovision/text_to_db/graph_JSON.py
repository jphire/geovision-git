import math
import json
from geovision.viz.models import *
from django.db.models import Q


class NodeEdgeJSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, Node) or isinstance(o, Edge):
			return o.dict
		return json.JSONEncoder.default(self, o)

class Node:
	def __init__(self, dataobject):
		self.dict = {}
		self.dict["data"] = {}
		if isinstance(dataobject, DbEntry):
			self.type = "db_entry"
			self.dict["id"] = dataobject.db_id
			self.dict["name"] = dataobject.db_id
			self.dict["data"]["source"] = dataobject.source_file
			self.dict["data"]["description"] = dataobject.description
			self.dict["data"]["type"] = "dbentry"

			if dataobject.source_file == "uniprot":
				self.dict["data"]["sub_db"] = dataobject.sub_db
				self.dict["data"]["entry_name"] = dataobject.entry_name
				self.dict["data"]["os_field"] = dataobject.os_field
				self.dict["data"]["other_info"] = dataobject.other_info
		elif isinstance(dataobject, Read):
			self.type = "read"
			self.dict["id"] = dataobject.read_id
			self.dict["name"] = dataobject.read_id
			self.dict["data"]["description"] = dataobject.description
			self.dict["data"]["type"] = "read"
		elif isinstance(dataobject, DbUniprotEcs):
			self.type = 'enzyme'
			self.dict['name'] = self.dict['id'] = dataobject.ec
			self.dict['data']['type'] = 'enzyme'
			self.dict['data']['$color'] = '#0000ff'
		else:
			raise Exception("parameter class must be Read, DbEntry or DbUniProtEcs")
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
	MAX_BITSCORE = 6000
	def __init__(self, nodeTo, blastobject):
		if nodeTo is None:
			raise Exception("Must supply nodeTo parameter")
		self.dict = {}
		self.dict["data"] = {}
		if isinstance(blastobject, Blast):
			self.dict["nodeTo"] = nodeTo.id
			self.dict["data"]["read"] = blastobject.read_id
			self.dict["data"]["database_name"] = blastobject.database_name
			self.dict["data"]["db_entry"] = blastobject.db_entry_id
			self.dict["data"]["length"] = blastobject.length
			self.dict["data"]["id"] = blastobject.id
#			self.dict["data"]["pident"] = blastobject.pident
#			self.dict["data"]["mismatch"] = blastobject.mismatch
#			self.dict["data"]["gapopen"] = blastobject.gapopen
#			self.dict["data"]["qstart"] = blastobject.qstart
#			self.dict["data"]["qend"] = blastobject.qend
#			self.dict["data"]["sstart"] = blastobject.sstart
#			self.dict["data"]["send"] = blastobject.send
			self.dict["data"]["error_value"] = blastobject.error_value
			self.dict["data"]["bitscore"] = blastobject.bitscore
############## Graph visualization style options below ################
# use these only to override, defaults in graphviz.js
#			self.dict["data"]["$type"] = "arrow"
#			self.dict["data"]["$dim"] = 15
#			self.dict["data"]["$lineWidth"] = 2
#			self.dict["data"]["$alpha"] = 1
#			self.dict["data"]["$epsilon"] = 7
		elif isinstance(blastobject, DbUniprotEcs):
			self.dict['nodeTo'] = nodeTo.ec
			self.dict['data']['$color'] = '#0000ff'
		else:
			raise Exception("Second parameter must be a blast or uniprot ecs object, is " + str(blastobject.__class__))

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
				if ec_number is None:
					raise Exception("Either db_entry or read parameter must be supplied")
				else:
					self.startpoint = NodeId(ec_number, "enzyme")
			else:
				self.startpoint = NodeId(read, "read")
		else:
			if read is not None or ec_number is not None:
				raise Exception("Cannot use both read and db_entry as a starting point")
			self.startpoint = NodeId(db_entry, "db_entry")
		self.startnode = self.get_node(self.startpoint)
		self.build_graph(self.startnode, self.depth_limit)

	def build_graph(self, startnode, maxdepth):
		self.nodes.append(startnode)
		self.build_graph_level([startnode], 1, maxdepth)
		self.add_ec_nodes()

	def build_graph_level(self, nodes, depth, maxdepth):
		if depth <= maxdepth:
			for node in nodes:
				queryset = self.make_blast_queryset(node)
				next_level_nodes = self.add_edges(node, queryset)
				self.build_graph_level(next_level_nodes, depth + 1, maxdepth)

	def add_ec_nodes(self):
		db_ids = []
		for node in self.nodes:
			if node.dict['data']['type'] == 'dbentry':
				db_ids.append(node.dict['id'])

		ecs = DbUniprotEcs.objects.filter(db_id__in=db_ids).filter(~Q(ec='?'))
		for ec in ecs:
			ecnode = Node(ec)
			ecid = self.get_node_id(ecnode)
			if ecnode not in self.nodes:
				self.nodes.append(ecnode)
			self.find_node_by_id(ec.db_id_id).dict["adjacencies"].append(Edge(ec, ec))

	def find_node_by_id(self, id): # XXX - linear search, change self.nodes to a dict!
		for n in self.nodes:
			if id == n.dict['id']:
				return n
		raise KeyError(repr(id))

	def make_enzyme_query(self, param = None):

		db_list = []
		db_query = DbUniprotEcs.objects.filter(ec = param.dict["id"])
		for line in db_query:
			if line.db_id not in db_list:
				raise Exception("test1 exception" + line.db_id)
				node = DbEntry.objects.get(db_id = line.db_id)
				raise Exception("test1 exception")
				db_list.append(line.db_id)

		db_entrys = Blast.objects.filter(db_entry__in = db_list)
		return db_entrys

	def make_blast_queryset(self, param = None):
		"""
		Function for making the blast table QuerySet. Takes only one parameter,
		an instance of Node object. Other query parameters are
		carried over as class parameters.

		Makes a QuerySet by stacking filters to an initial unfiltered QuerySet
		object. Returns an unevaluated QuerySet object, thus the actual db query
		is not made in this function.
		"""
		query = Blast.deferred()
#		if param_type == "enzyme":
#			query = query.filter(ec_number = param.dict["id"])
		if param.type == "db_entry":
			query = query.filter(db_entry = param.dict["id"])
		elif param.type == "read":
			query = query.filter(read = param.dict["id"])
		else:
			query = self.make_enzyme_query(param)
		query = query.filter(error_value__lte = self.e_value_limit)
		query = query.filter(bitscore__gte = self.bitscore_limit)
		query = query.order_by('-bitscore')
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
		startnode_id = self.get_node_id(startnode)
		if startnode.type == "db_entry":
			reads = Read.deferred().filter(pk__in=map(lambda blast: blast.read_id, queryset))

			for (read, blast) in zip(reads, queryset):
				readnode = Node(read)
				readid = self.get_node_id(readnode)
				if readnode not in self.nodes:
					self.nodes.append(readnode)
					next_level_nodes.add(readnode)
				startnode.dict["adjacencies"].append(Edge(readid, blast))

		elif startnode.type is "read" or startnode.type is "enzyme":
			db_entries = DbEntry.deferred().filter(pk__in=map(lambda blast: blast.db_entry_id, queryset))

			for (dbentry, blast) in zip(db_entries, queryset):
				dbnode = Node(dbentry)
				db_id = self.get_node_id(dbnode)
				if dbnode not in self.nodes:
					self.nodes.append(dbnode)
					next_level_nodes.add(dbnode)
				startnode.dict["adjacencies"].append(Edge(db_id, blast))
		else:
			raise Exception("startnode type must be db_entry or read")
		return next_level_nodes

	def get_node(self, node_id):
		if node_id.type is "read":
			return Node(Read.objects.get(read_id = node_id.id))
		elif node_id.type is "db_entry":
			return Node(DbEntry.objects.get(db_id = node_id.id))
		elif node_id.type is "enzyme":
			query=DbUniprotEcs.objects.filter(ec = node_id.id)[:1]
			for q in query:
				return Node(q)
		else:
			raise Exception("Invalid node_id parameter, must be tuple (type, id)")

	def get_node_id(self, node):
		if node.type == "db_entry":
			return NodeId(node.dict["id"], "db_entry")
		elif node.type == "read":
			return NodeId(node.dict["id"], "read")
		elif node.type == "enzyme":
			return NodeId(node.dict["id"], "enzyme")
		else:
			raise Exception("Invalid node parameter, must be Node of type read or db_entry or enzyme")

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
