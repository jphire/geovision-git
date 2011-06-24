# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="sundo"
__date__ ="$Jun 16, 2011 5:45:47 PM$"

import unittest
import uniprot_ecs_parser
from geovision.settings import PROJECT_PATH
from os import path

TEST_FILE_PATH = PROJECT_PATH + '/text_to_db/testfiles/'

class Test_Uniprot_Ecs_parser(unittest.TestCase):
	def test_ecs_parse_first(self):
		parser = uniprot_ecs_parser.EcsFileParser(TEST_FILE_PATH + "test_uniprot.ecs")
		entries = list(parser.next_ecs_entry())
		self.assertEqual(len(entries), 1)
		entry = entries[0]
		self.assertEqual(entry.db_id, 'Q91G55')
		self.assertEqual(entry.protein_existence_type, 'P')
		self.assertEqual(entry.ec, '?')

	def test_ecs_parse_second(self):
		parser = uniprot_ecs_parser.EcsFileParser(TEST_FILE_PATH + "test_uniprot.ecs")
		parser.next_ecs_entry()
		entries = list(parser.next_ecs_entry())
		self.assertEqual(len(entries), 2)
		entry1 = entries[0]
		self.assertEqual(entry1.db_id, 'P27365')
		self.assertEqual(entry1.protein_existence_type, 'ET')
		self.assertEqual(entry1.ec, '5.3.3.1')
		entry2 = entries[1]
		self.assertEqual(entry2.db_id, 'P27365')
		self.assertEqual(entry2.protein_existence_type, 'ET')
		self.assertEqual(entry2.ec, '1.1.1.145')

	def test_ecs_parse_past_the_end(self):
		parser = uniprot_ecs_parser.EcsFileParser(TEST_FILE_PATH + "test_uniprot.ecs")
		parser.next_ecs_entry()
		parser.next_ecs_entry()
		entry = parser.next_ecs_entry()
		self.assertEqual(entry, None)
