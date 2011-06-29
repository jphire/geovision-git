import unittest
import text_to_db.uniprot_ecs_parser as uniprot_ecs_parser
from geovision.settings import TEST_FILE_PATH


class UniprotEcsParserTests(unittest.TestCase):
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
