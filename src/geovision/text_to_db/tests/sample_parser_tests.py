#coding: UTF-8

import unittest
import text_to_db.sample_parser as sample_parser
from geovision.settings import TEST_FILE_PATH

class SampleParserTests(unittest.TestCase):
	#def setUp(self):
    #    self.foo = Test_sample_parser()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

	def test_sample_parse_first(self):
		parser = sample_parser.SamplefileParser(TEST_FILE_PATH + "sample_test.txt")
		read = parser.next_read()
		self.assertEqual(read.read_id, 'ensimmainen')
		self.assertEqual(read.description, 'seliseli')
		self.assertEqual(read.data, 'ASDFASEGAASGEASGASG')

	def test_sample_parse_last(self):
		parser = sample_parser.SamplefileParser(TEST_FILE_PATH + "sample_test.txt")
		parser.next_read()
		read = parser.next_read()
		self.assertEqual(read.read_id, 'toinen')
		self.assertEqual(read.description, 'sulisuli')
		self.assertEqual(read.data, 'ASGEAGSGASEGAG')

	def test_sample_parse_past_the_end(self):
		parser = sample_parser.SamplefileParser(TEST_FILE_PATH + "sample_test.txt")
		parser.next_read()
		parser.next_read()
		read = parser.next_read()
		self.assertEqual(read, None)

if __name__ == '__main__':
	unittest.main()
