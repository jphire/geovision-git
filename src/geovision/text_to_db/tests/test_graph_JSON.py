import unittest
from geovision.text_to_db.graph_JSON import *
import json

def create_blast(**kwargs):
	kwargs['read'] = Read.objects.get(pk=kwargs['read'])
	kwargs['db_entry'] = DbEntry.objects.get(pk=kwargs['db_entry'])
	Blast.objects.create(**kwargs)

class Test_graph_JSONTestCase(unittest.TestCase):

	def setUp(self):
		Read.objects.all().delete()
		Read.objects.create(sample="SMPL1", read_id="R1", description="bazz", data='ASD')
		Read.objects.create(sample="SMPL2", read_id="R2", description="baz", data='ASD')
		Read.objects.create(sample="SMPL3", read_id="R3", description="baz", data='ASD')
		Read.objects.create(sample="SMPL4", read_id="R4", description="baz", data='ASD')
		Read.objects.create(sample="SMPL3", read_id="R5", description="baz", data='ASD')
		Read.objects.create(sample="SMPL2", read_id="R6", description="baz", data='ASD')

		DbEntry.objects.all().delete()
		DbEntry.objects.create(source_file = "uniprot", db_id = "DB1", description="quix", data='ASD', sub_db="sub", entry_name = "entryname", os_field="osfield", other_info = "otherinfo")
		DbEntry.objects.create(source_file = "frnadb", db_id = "DB2", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "frnadb", db_id = "DB3", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "frnadb", db_id = "DB4", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "frnadb", db_id = "DB5", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "frnadb", db_id = "DB6", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "frnadb", db_id = "DB7", description="quux", data='ASD')

		create_blast(read="R1", database_name = "uniprot", db_entry="DB1", error_value=0.005, bitscore=200, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", database_name = "uniprot", db_entry="DB2", error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", database_name = "uniprot", db_entry="DB3", error_value=0.005, bitscore=600, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", database_name = "uniprot", db_entry="DB4", error_value=0.005, bitscore=800, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R2", database_name = "uniprot", db_entry="DB1", error_value=0.005, bitscore=1000, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R3", database_name = "uniprot", db_entry="DB1", error_value=0.005, bitscore=300, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R4", database_name = "uniprot", db_entry="DB2", error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R5", database_name = "uniprot", db_entry="DB3", error_value=0.005, bitscore=700, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", database_name = "uniprot", db_entry="DB4", error_value=0.005, bitscore=1100, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", database_name = "uniprot", db_entry="DB5", error_value = 0.005, bitscore=1500, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)

	def test_node_init_fail_1(self):
		self.assertRaises(Exception, Node, "moo")

	def test_node_init_1(self):
		n = Node(Read.objects.get(read_id="R1"))
		self.assertEquals(n.dict["id"], "R1")
		self.assertEquals(n.dict["name"], "R1")
		self.assertEquals(n.dict["data"]["description"], "bazz")

	def test_node_init_2(self):
		n = Node(DbEntry.objects.get(db_id="DB1"))
		self.assertEquals(n.dict["id"], "DB1")
		self.assertEquals(n.dict["name"], "DB1")
		self.assertEquals(n.dict["data"]["description"], "quix")
		self.assertEquals(n.dict["data"]["source"], "uniprot")
		self.assertEquals(n.dict["data"]["sub_db"], "sub")
		self.assertEquals(n.dict["data"]["entry_name"], "entryname")
		self.assertEquals(n.dict["data"]["os_field"], "osfield")
		self.assertEquals(n.dict["data"]["other_info"], "otherinfo")

	def test_node_repr_1(self):
		n = Node(DbEntry.objects.get(db_id="DB1"))
		self.assertEquals(n.__repr__(), '{"adjacencies": [], "data": {"description": "quix", "other_info": "otherinfo", "sub_db": "sub", "source": "uniprot", "os_field": "osfield", "entry_name": "entryname", "type": "dbentry"}, "id": "DB1", "name": "DB1"}')

	def test_edge_init_fail_1(self):
		self.assertRaises(Exception, Edge, "R1", "moo")

	def test_edge_init_1(self):
		b = Blast.objects.all()[:1]
		e = Edge(NodeId("R1", "read"), b[0])
		self.assertEquals(e.dict["nodeTo"], "R1")
		self.assertEquals(e.dict["data"]["read"], "R1")
		self.assertEquals(e.dict["data"]["database_name"], "uniprot")
		self.assertEquals(e.dict["data"]["db_entry"], "DB1")
		self.assertEquals(e.dict["data"]["length"], 20)
		self.assertAlmostEquals(e.dict["data"]["error_value"], 0.005)
		self.assertEquals(e.dict["data"]["bitscore"], 200)
#		self.assertEquals(e.dict["data"]["$color"], "#ff0000")
#		self.assertEquals(e.dict["data"]["$type"], "arrow")

	def test_edge_repr_1(self):
		b = Blast.objects.all()[:1]
		e = Edge(NodeId("R1", "read"), b[0])
		self.assertEquals(e.__repr__(), '{"nodeTo": "R1", "data": {"error_value": 0.0050000000000000001, "bitscore": 200.0, "read": "R1", "database_name": "uniprot", "length": 20, "db_entry": "DB1", "id": 1}}')

	def test_nodeid(self):
		a = NodeId("12345", "test")
		b = NodeId("12345", "test")
		c = NodeId("asdf", "test")
		self.assertEqual(a.id, "12345")
		self.assertEqual(b.type, "test")
		self.assertEqual(a, b)
		self.assertNotEqual(a, c)

	def test_query_to_json_init_fail_1(self):
		self.assertRaises(Exception, QueryToJSON, db_entry="DB1", read="R1")

	def test_query_to_json_init_fail_2(self):
		self.assertRaises(Exception, QueryToJSON, ec_number="1.1.1.1")

	def test_query_to_json_init_1(self):
		q = QueryToJSON(db_entry = "DB2")
		self.assertEquals(q.startnode, Node(DbEntry.objects.get(db_id = "DB2")))
		self.assertEquals(q.startpoint, NodeId("DB2", "db_entry"))
		self.assertEquals(q.e_value_limit, 1)
		self.assertEquals(q.bitscore_limit, 0)
		self.assertEquals(q.depth_limit, 2)
		self.assertEquals(q.max_amount, 5)

	def test_query_to_json_init_2(self):
		q = QueryToJSON(read = "R1", e_value_limit=0.002, bitscore_limit=300)
		self.assertEquals(q.startnode, Node(Read.objects.get(read_id = "R1")))
		self.assertEquals(q.startpoint, NodeId("R1", "read"))
		self.assertEquals(q.e_value_limit, 0.002)
		self.assertEquals(q.bitscore_limit, 300)
		self.assertEquals(q.depth_limit, 2)
		self.assertEquals(q.max_amount, 5)

#	def test_query_to_json_dict_1(self):
#		q = QueryToJSON(read = "R1", e_value_limit=0.006, bitscore_limit=1000)
#		self.assertEquals(str(q), "")

if __name__ == '__main__':
    unittest.main()

