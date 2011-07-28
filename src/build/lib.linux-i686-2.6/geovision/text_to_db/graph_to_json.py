# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jjlaukka"
__date__ ="$Jun 27, 2011 8:52:05 PM$"

import json
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geovision.settings'
from geovision.viz.models import *
from geovision.settings import PROJECT_PATH

class JsonCreator:
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
		self.node_list = []
		if db_entry is None:
			if read is None:
				raise Exception("Either db_entry or read parameter must be supplied")
			else:
				self.startpoint = ("R1")
		else:
			self.startpoint = ("DB1")
		self.startnode = "DB1"

	def make_blast_queryset(self):
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
		if self.db_entry is not None:
			query = query.filter(db_entry__db_id = self.db_entry)
		elif self.read is not None:
			query = query.filter(read__read_id = self.read)
		else:
			return None
		query = query.filter(error_value__lte = self.e_value_limit)
		query = query.filter(bitscore__gte = self.bitscore_limit)
		query = query.order_by('bitscore', 'error_value')
		return query[:self.max_amount]


	def build_adjacency_lists(self):

		query = self.make_blast_queryset()
#		json_file = open(PROJECTROOT + "/static/json_test_file.js", 'w')
#		json_file.write("" + str(query.count()) +  "\n")

		nodes_this_level = []
		for blastitem in query:
			if blastitem.read.read_id not in self.nodes:
				self.add_new_read(blastitem)
				if self.db_entry is not None:
					nodes_this_level.append(blastitem.read.read_id)
			self.add_db_adj(blastitem)

			if blastitem.db_entry.db_id not in self.nodes:
				self.add_new_db(blastitem)
				if self.read is not None:
					nodes_this_level.append(blastitem.db_entry.db_id)
			self.add_read_adj(blastitem)
#		json_file.write("" + str(nodes_this_level) +  "\n")
		return nodes_this_level

	def add_new_read(self, blastitem):
		self.nodes[blastitem.read.read_id] = {'name':blastitem.read.read_id, 'id':blastitem.read.read_id, 'data':{}, 'adjacencies':[]}
		description = self.make_read_query(blastitem.read.read_id).description
		data = {'description':description, 'bitscore':blastitem.bitscore, 'read_seq':blastitem.read_seq, 'db_seq':blastitem.db_seq, '$type':'circle'}
		self.nodes[blastitem.read.read_id]['data'] = data

	def add_db_adj(self, blastitem):
		color = self.bitscore_to_hex(blastitem.bitscore)
		str = {'nodeTo' : blastitem.db_entry.db_id, 'data' : {'$color':color, 'color':color, '$type':'line'}}
		self.nodes[blastitem.read.read_id]['adjacencies'].append(str)

	def add_new_db(self, blastitem):
		self.nodes[blastitem.db_entry.db_id] = {'name':blastitem.db_entry.db_id, 'id':blastitem.db_entry.db_id, 'data':{}, 'adjacencies':[]}
		description = self.make_db_query(blastitem.db_entry.db_id).description
		data = {'description':description, 'bitscore':blastitem.bitscore, 'read_seq':blastitem.read_seq, 'db_seq':blastitem.db_seq, '$type':'triangle'}
		self.nodes[blastitem.db_entry.db_id]['data'] = data

	def add_read_adj(self, blastitem):
		color = self.bitscore_to_hex(blastitem.bitscore)
		str = {'nodeTo' : blastitem.read.read_id, 'data' : {'$color':color, 'color':color, '$type':'line'}}
		self.nodes[blastitem.db_entry.db_id]['adjacencies'].append(str)

	def build_graph(self, maxdepth):

		depth = 0
		node_list = []
		sumlist = []
		node_list.append(self.startnode)
		#json_file = open(PROJECTROOT + "/static/json_test_graph.js", 'w')

		while depth < maxdepth:
			#json_file.write("" + str(node_list) +  "\n")
			for node in node_list:
				sumlist = sumlist + self.build_adjacency_lists()

			node_list = sumlist
			#json_file.write("" + str(node_list) +  "\n")
			sumlist = []

			if self.read is None:
				self.db_entry = None
				self.read = node_list[0]
			elif self.db_entry is None:
				self.read = None
				self.db_entry = node_list[0]
			depth = depth + 1

		return 0

	def make_read_query(self, read):
		return Read.objects.get(read_id = read)

	def make_db_query(self, db_entry):
		return DbEntry.objects.get(db_id = db_entry)

	def get_graph(self):
		return self.nodes

	def write_to_json(self):

		for k, v in self.nodes.iteritems():
			self.node_list.append(v)
			
		json_file = open(PROJECT_PATH + "/static/json_test_graph.js", 'w')
		json_file.write("var json_data = \n")
		json.dump(self.node_list, json_file)
		json_file.close()

	def bitscore_to_hex(self, bitscore):
		if 0 < bitscore < 100:
			return '#C0C0C0'

		elif 100 <= bitscore < 500:
			return '#FFFF00'

		elif 500 <= bitscore < 1000:
			return '#0000FF'

		elif 1000 <= bitscore:
			return '#00FF00'

		else:
			return 'error'

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


if __name__ == "__main__":
    print "Hello World"
