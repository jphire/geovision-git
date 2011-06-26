import json
from usbcreator.remtimest import max_age
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import *
from geovision.settings import PROJECTROOT

class QueryToJSON:
	"""
	Makes a query according to the parameters and generates graph JSON file
	from the fetched data.
	Nodes and edges are kept in a dictionary with node_ids as keys.
	Dictionary format is:
	self.nodes[node_id] = [node, set(tuple(edge_to, Blast), tuple(edge_to, Blast), ...)]

	Currently assumes that both Read.read_id and DbEntry.db_id can identify
	unique row from the table, this approach may cause problems later.
	"""
	def __init__(self, ec_number=None, db_entry=None, read=None,
				e_value_limit=None, bitscore_limit=None, depth_limit=2,
				max_amount=5):
		self.ec_number = ec_number
		self.db_entry = db_entry
		self.read = read
		self.e_value_limit = 1 if e_value_limit is None else e_value_limit
		self.bitscore_limit = 0 if bitscore_limit is None else bitscore_limit
		self.depth_limit = depth_limit
		self.max_amount = max_amount
		self.nodes = {}
		if db_entry is None:
			if read is None:
				raise Exception("Either db_entry or read parameter must be supplied")
			else:
				self.startpoint = (read, "read")
		else:
			self.startpoint = (db_entry, "db_entry")
		self.startnode = self.get_node(self.startpoint)

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
		query = query.order_by('bitscore', 'error_value')
		return query[:self.max_amount]

	def build_graph(self, startnode, depth):
		queryset = self.make_blast_queryset(startnode)
		self.nodes[self.get_node_id(startnode)] = [startnode, set()]

#		for blastitem in nodes_this_level():
#			if blastitem.read not in self.nodes:
#				self.nodes[blastitem.read] = set()
#				nodes_this_level.add(blastitem_read)
#			self.nodes[blastitem.read].add(blastitem.db_entry)
#			if blastitem.db_entry not in self.nodes:
#				self.nodes[blastitem.db_entry] = set()
#				nodes_this_level.add(blastitem.db_entry)
#			self.nodes[blastitem.db_entry].add(blastitem.read)

		return 0

	def add_edges(self, startnode, queryset):
		if startnode.__class__ is DbEntry:
			for edge in queryset:
				readid = (edge.read, "read")
				if readid not in self.nodes:
					self.nodes[readid] = [Read.objects.get(read_id = edge.read), set()]
				self.nodes[self.get_node_id(startnode)][1].add((readid, edge))
		elif startnode.__class__ is Read:
			for edge in queryset:
				db_id = (edge.db_entry, "db_entry")
				if db_id not in self.nodes:
					self.nodes[db_id] = [DbEntry.objects.get(db_id = edge.db_entry), set()]
				self.nodes[self.get_node_id(startnode)][1].add((db_id, edge))


	def build_graph_level(self, depth, maxdepth):
		queryset = self.make_blast_queryset()
		return 0

	def get_node(self, node_id):
		if node_id[1] is "read":
			return Read.objects.get(read_id = node_id[0])
		elif node_id[1] is "db_entry":
			return DbEntry.objects.get(db_id = node_id[0])
		else:
			raise Exception("Invalid node_id parameter, must be tuple (type, id)")

	def get_node_id(self, node):
		if node.__class__ is DbEntry:
			return (node.db_id, "db_entry")
		elif node.__class__ is Read:
			return (node.read_id, "read")
		else:
			raise Exception("Invalid node parameter, must be Read or DbEntry")
			
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
#    json_file = open(PROJECTROOT + "/static/json_test_file.js", 'w')
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