#To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from geovision.text_to_db.graph_JSON import *
from geovision.text_to_db.create_JSON import *
from geovision.viz.models import *
import json

class  Test_graph_JSONTestCase(unittest.TestCase):

	def setUp(self):

		read1 = Read.objects.get(read_id="R1")
		read2 = Read.objects.get(read_id="R2")
		read3 = Read.objects.get(read_id="R3")
		read4 = Read.objects.get(read_id="R4")
		read5 = Read.objects.get(read_id="R5")
		read6 = Read.objects.get(read_id="R6")

		db_entry1 = DbEntry.objects.get(db_id="DB1")
		db_entry2 = DbEntry.objects.get(db_id="DB2")
		db_entry3 = DbEntry.objects.get(db_id="DB3")
		db_entry4 = DbEntry.objects.get(db_id="DB4")
		db_entry5 = DbEntry.objects.get(db_id="DB5")
		db_entry6 = DbEntry.objects.get(db_id="DB6")
		db_entry7 = DbEntry.objects.get(db_id="DB7")


		Blast.objects.create(read=read1, db_entry = db_entry1, error_value = 0.005, bitscore=200, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read=read2, db_entry = db_entry2, error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read=read1, db_entry = db_entry3, error_value=0.005, bitscore=600, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read=read3, db_entry = db_entry4, error_value=0.005, bitscore=800, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read=read2, db_entry=db_entry1, error_value=0.005, bitscore=1000, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read=read3, db_entry=db_entry1, error_value=0.005, bitscore=200, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read=read4, db_entry=db_entry2, error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read=read5, db_entry=db_entry3, error_value=0.005, bitscore=700, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read=read1, db_entry=db_entry4, error_value=0.005, bitscore=1100, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
		Blast.objects.create(read=read1, db_entry=db_entry5, error_value = 0.005, bitscore=1500, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)

	def test_create_JSON(self):
		print Blast.objects.filter(db_entry="DB1")
		graph = QueryToJSON(None, "DB1", None, 1, 0, 2, 5)
		graph.build_graph(2)
		graph.write_to_json()

		assert 1==1
        

if __name__ == '__main__':
    unittest.main()

