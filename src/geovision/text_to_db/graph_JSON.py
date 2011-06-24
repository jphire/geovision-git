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
	Nodes are kept in a dictionary, edges are added to sets which are linked to
	nodes.
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
		self.startpoint = db_entry if db_entry is not None else read

	def make_blast_query(self, db_entry_param = self.db_entry, read_param = self.read):
		query = Blast.objects.all()
#		if self.ec_number is not None:
#			query = query.filter(ec_number = self.ec_number)
		if db_entry_param is not None:
			query = query.filter(db_entry = db_entry_param)
		if read_param is not None:
			query = query.filter(read = read_param)
		query = query.filter(error_value__lte = self.e_value_limit)
		query = query.filter(bitscore__gte = self.bitscore_limit)
		query = query.order_by('bitscore', 'error_value')
		return query[:self.max_amount]

	def build_adjacency_lists(self):
		query = self.make_blast_query()
		nodes_this_level = set()
		for blastitem in query:
			if blastitem.read not in self.nodes:
				self.nodes[blastitem.read] = set()
				nodes_this_level.add(blastitem_read)
			self.nodes[blastitem.read].add(blastitem.db_entry)
			if blastitem.db_entry not in self.nodes:
				self.nodes[blastitem.db_entry] = set()
				nodes_this_level.add(blastitem.db_entry)
			self.nodes[blastitem.db_entry].add(blastitem.read)

		return 0

	def build_adjacency_list_level(self, depth, maxdepth):

		return 0

	def make_read_query(self, read):
		return Read.objects.filter(read_id = read)[:1]


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
