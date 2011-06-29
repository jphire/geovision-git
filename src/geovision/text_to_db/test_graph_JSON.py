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
		Read.objects.create(sample="SMPL1", read_id="R1", description="baz", data='ASD')
		Read.objects.create(sample="SMPL2", read_id="R2", description="baz", data='ASD')
		Read.objects.create(sample="SMPL3", read_id="R3", description="baz", data='ASD')
		Read.objects.create(sample="SMPL4", read_id="R4", description="baz", data='ASD')
		Read.objects.create(sample="SMPL3", read_id="R5", description="baz", data='ASD')
		Read.objects.create(sample="SMPL2", read_id="R6", description="baz", data='ASD')

		DbEntry.objects.all().delete()
		DbEntry.objects.create(source_file = "uniprot", db_id = "DB1", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "uniprot", db_id = "DB2", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "uniprot", db_id = "DB3", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "uniprot", db_id = "DB4", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "uniprot", db_id = "DB5", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "uniprot", db_id = "DB6", description="quux", data='ASD')
		DbEntry.objects.create(source_file = "uniprot", db_id = "DB7", description="quux", data='ASD')

		create_blast(read="R1", db_entry="DB1", error_value=0.005, bitscore=200, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", db_entry="DB2", error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", db_entry="DB3", error_value=0.005, bitscore=600, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", db_entry="DB4", error_value=0.005, bitscore=800, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R2", db_entry="DB1", error_value=0.005, bitscore=1000, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R3", db_entry="DB1", error_value=0.005, bitscore=200, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R4", db_entry="DB2", error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R5", db_entry="DB3", error_value=0.005, bitscore=700, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", db_entry="DB4", error_value=0.005, bitscore=1100, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		create_blast(read="R1", db_entry="DB5", error_value = 0.005, bitscore=1500, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)

	def test_node_id(self):
		a = NodeId("12345", "test")
		b = NodeId("12345", "test")
		c = NodeId("asdf", "test")
		assertEquals(a.id, "12345")
		assertEquals(b.type, "test")
		assertEquals(a, b)
		assertNotEqual(a, c)

	def test_query_to_json_init_1(self):
		q = QueryToJSON(db_entry="DB1", )


if __name__ == '__main__':
    unittest.main()

