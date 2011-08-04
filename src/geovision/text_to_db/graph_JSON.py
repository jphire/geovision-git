import json
from geovision.viz.models import *
from django.db.models import Q


class NodeEdgeJSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, Node) or isinstance(o, Edge):
			return o.dict
		return json.JSONEncoder.default(self, o)

class Node:
	"""
	This class represents a node in the graph. Node can be of following types:
	read, dbentry or enzyme. All information that a node has is put in a dictionary.
	All the node types have an attribute called adjacencies, which is a dict containing
	node's connections to other nodes in the graph. The information about the node is
	retrieved from the dataobjects given as an argument to the __init__ method.

	Node's certain value in dictionary can be changed as follows:
	node.dict['data']['description'] = "something"
	"""
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
			self.dict["data"]["source"] = dataobject.sample
		elif isinstance(dataobject, DbUniprotEcs) or isinstance(dataobject, BlastEcs):
			self.type = 'enzyme'
			self.dict['id'] = self.dict['name'] = dataobject.ec
			self.dict['data']['type'] = 'enzyme'
		else:
			raise Exception("parameter class must be Read, DbEntry, BlastEcs or DbUniprotEcs")
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
	"""
	This class represents a connection between two nodes in the graph. All infromation
	related to the edge is put in a dictionary. The information is retrieved from the blastobject
	that is given as an argument to the __init__ method. The information in the dict can be
	referenced as follows:

	edge.dict['data']['bitscore'] = some_int_value
	"""
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
			self.dict["data"]["blast_id"] = blastobject.id
			self.dict["data"]["error_value"] = blastobject.error_value
			self.dict["data"]["bitscore"] = blastobject.bitscore
		elif isinstance(blastobject, BlastEcs):
			self.dict['nodeTo'] = nodeTo.id
			self.dict['data']['bitscore'] = blastobject.bitscore
			self.dict['data']['error_value'] = blastobject.error_value
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
	Makes a query according to the parameters and generates a graph JSON file
	from the fetched data.

	Currently assumes that both Read.read_id and DbEntry.db_id are foreign keys.
	"""
	def __init__(self, enzyme=None, db_entry=None, read=None,
				e_value_limit=1, bitscore_limit=0, depth_limit=2,
				max_amount=5, offset=0, samples=[]):
		self.enzyme = enzyme
		self.db_entry = db_entry
		self.read = read
		self.e_value_limit = e_value_limit
		self.bitscore_limit = bitscore_limit
		self.depth_limit = depth_limit
		self.max_amount = max_amount
		self.offset = offset
		self.samples = samples
		self.nodes = []
		if db_entry is None:
			if read is None:
				if enzyme is None:
					raise Exception("Either db_entry or read parameter must be supplied")
				else:
					self.startpoint = NodeId(enzyme, "enzyme")
			else:
				self.startpoint = NodeId(read, "read")
		else:
			if read is not None or enzyme is not None:
				raise Exception("Cannot use both read and db_entry as a starting point")
			self.startpoint = NodeId(db_entry, "db_entry")
		self.startnode = self.get_node(self.startpoint)
		self.build_graph(self.startnode)

	def build_graph(self, startnode):
		"""
		The top level function that uses build_graph_level to add all nodes and edges 
		to the graph. The enzyme nodes and edges are added only after all the other nodes 
		and connections are added.
		"""
		self.nodes.append(startnode)
		self.build_graph_level([startnode], 1)
		self.add_ec_nodes()
		self.populate_ec_names()

	def build_graph_level(self, nodes, depth):
		"""
		Goes through all nodes given as an argument and asks make_blast_queryset for
		connections to other nodes. Then adds these connections to the graph through add_edges.
		Calls recursively itself until depth is greater than the maximum depth given. Thus the
		graph is build depth first.
		"""
		if depth <= self.depth_limit:
			for node in nodes:
				(count, queryset) = self.make_blast_queryset(node)
				node.dict['data']['hidden_nodes_count'] = count
				next_level_nodes = self.add_edges(node, queryset)
				self.build_graph_level(next_level_nodes, depth + 1)

	def add_ec_nodes(self):
		"""
		Adds enzyme nodes and edges to the graph. Enzyme nodes only have connections
		to database entry nodes.
		"""
		db_ids = []
		for node in self.nodes:
			if node.dict['data']['type'] == 'dbentry':
				db_ids.append(node.dict['id'])

		ecs = BlastEcs.objects.filter(db_entry__in=db_ids)
		# If enzyme-query, excludes root node from results
		if self.enzyme:
			ecs = ecs.filter(~(Q(ec=self.enzyme)))
		for ec in ecs:
			ecnode = Node(ec)
			ecid = self.get_node_id(ecnode)
			if ecnode not in self.nodes:
				self.nodes.append(ecnode)
			self.find_node_by_id(ec.db_entry_id).dict["adjacencies"].append(Edge(ecid, ec))

	def populate_ec_names(self):
		"""
		Adds enzyme's other names info to all the enzyme nodes in the graph.
		"""
		for node in self.nodes:
			if node.dict['data']['type'] == 'enzyme':
				try:
					node.dict['data']['name'] = EnzymeName.objects.filter(ec_number=node.dict['id']).order_by('id')[0].enzyme_name
				except IndexError:
					pass

	def find_node_by_id(self, id): 
		"""
		Returns a node in the graph based on it's id.
		"""
		for n in self.nodes:
			if id == n.dict['id']:
				return n
		raise KeyError(repr(id))

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

		if param.type == "db_entry":
			query = query.filter(db_entry=param.dict["id"]).select_related('read').defer(*('read__' + x for x in Read.deferred_fields))
			query = query.filter(read__sample__in=['ABLU'])
		elif param.type == "read":
			query = query.filter(read=param.dict["id"]).select_related('db_entry').defer(*('db_entry__' + x for x in DbEntry.deferred_fields))

		elif param.type == "enzyme":
			query = BlastEcs.objects.filter(ec=param.dict["id"]).select_related('db_entry').defer(*('db_entry__' + x for x in DbEntry.deferred_fields))
		else:
			raise RuntimeError('bad param type "%s"' % (param.type,))
		
		query = query.filter(error_value__lte = self.e_value_limit)
		query = query.filter(bitscore__gt = self.bitscore_limit)
		if self.offset != 0:
				query = query.filter(bitscore__lt = self.offset)
		query = query.order_by('-bitscore')
		count = query.count() - self.max_amount
		if count < 0:
			count = 0
		return (count, query[:self.max_amount])

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
				read = blast.read
				readnode = Node(read)
				readid = self.get_node_id(readnode)
				if readnode not in self.nodes:
					self.nodes.append(readnode)
					next_level_nodes.add(readnode)
				startnode.dict["adjacencies"].append(Edge(readid, blast))

		elif startnode.type in ("read", "enzyme"):
			for blast in queryset:
				dbentry = blast.db_entry
				dbnode = Node(dbentry)
				db_id = self.get_node_id(dbnode)
				if dbnode not in self.nodes:
					self.nodes.append(dbnode)
					next_level_nodes.add(dbnode)
				startnode.dict["adjacencies"].append(Edge(db_id, blast))
		else:
			raise Exception("startnode type must be db_entry or read or enzyme")
		return next_level_nodes

	def get_node(self, node_id):
		"""
		Returns a Node object based on the given node_id argument's types.
		"""
		if node_id.type is "read":
			return Node(Read.objects.get(read_id = node_id.id))
		elif node_id.type is "db_entry":
			return Node(DbEntry.objects.get(db_id = node_id.id))
		elif node_id.type is "enzyme":
			query = DbUniprotEcs.objects.filter(ec = node_id.id)[:1]
			if not query:
				raise Exception('Enzyme not found')
			return Node(query[0])
		else:
			raise Exception("Invalid node_id parameter, must be tuple (type, id)")

	def get_node_id(self, node):
		"""
		Returns node's id.
		"""
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
		"""
		Used only for testing and dumping the JSON model of the graph to a file.
		"""
		json_file = None
		try:
			json_file = open(PROJECTROOT + file, 'w')
		except NameError:
			json_file = open(file, 'w')
		json_file.write(str(self.nodes))
		json_file.close()
		
	def __repr__(self):
		return str(self.nodes)
