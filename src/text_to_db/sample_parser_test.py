# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
import psycopg2

connection = None
cursor = None

class  Sample_parser_TestCase(unittest.TestCase):
	def setUp(self):
		connection = psycopg2.connect("dbname=tkt_gviz user=tkt_gviz")
		cursor = connection.cursor()

	def tearDown(self):
		cursor.close()
		connection.close()

	def test_sample_parser_(self):
		cursor.execute("INSERT INTO viz_read (source_file")
		#assert x != y;
		#self.assertEqual(x, y, "Msg");
		self.fail("TODO: Write test")

if __name__ == '__main__':
	unittest.main()

