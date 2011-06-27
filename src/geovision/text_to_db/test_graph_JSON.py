#To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from geovision.text_to_db.graph_JSON import *
from geovision.text_to_db.create_JSON import *
from geovision.viz.models import *
import json

class  Test_graph_JSONTestCase(unittest.TestCase):

	def setUp(self):
		Blast.objects.create(read="R1", db_entry="DB1", error_value=0.005, bitscore=200, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read="R1", db_entry="DB2", error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read="R1", db_entry="DB3", error_value=0.005, bitscore=600, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read="R1", db_entry="DB4", error_value=0.005, bitscore=800, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read="R2", db_entry="DB1", error_value=0.005, bitscore=1000, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read="R3", db_entry="DB1", error_value=0.005, bitscore=200, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read="R4", db_entry="DB2", error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read="R5", db_entry="DB3", error_value=0.005, bitscore=700, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read="R1", db_entry="DB4", error_value=0.005, bitscore=1100, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read="R1", db_entry="DB5", error_value = 0.005, bitscore=1500, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)


	def test_create_JSON(self):
		print Blast.objects.filter(db_entry="DB1")
		graph = QueryToJSON(None, "DB1", None, 1, 0, 2, 5)
		graph.build_graph(2)
		graph.write_to_json()

		assert 1==1
        

if __name__ == '__main__':
    unittest.main()

