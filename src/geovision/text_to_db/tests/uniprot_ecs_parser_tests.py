import unittest
import text_to_db.uniprot_ecs_parser as uniprot_ecs_parser
import run_db_parser
from geovision.settings import TEST_FILE_PATH
from viz.models import DbUniprotEcs as EcsEntry, DbEntry


class UniprotEcsParserTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		DbEntry.objects.all().delete()
		run_db_parser.run(['argv0', TEST_FILE_PATH + 'db_test_uniprot.fasta', 'uniprot'])

	def setUp(self):
		self.parser = uniprot_ecs_parser.EcsFileParser(TEST_FILE_PATH + "test_uniprot.ecs")

	def test_ecs_parse_first(self):
		entries = list(self.parser.next_ecs_entry())
		self.assertEqual(len(entries), 1)
		entry = entries[0]
		self.assertEqual(entry.db_id.db_id, 'Q197F8')
		self.assertEqual(entry.protein_existence_type, 'P')
		self.assertEqual(entry.ec, '?')

	def test_ecs_parse_second(self):
		self.parser.next_ecs_entry()
		entries = list(self.parser.next_ecs_entry())
		self.assertEqual(len(entries), 2)
		entry1 = entries[0]
		self.assertEqual(entry1.db_id.db_id, 'Q197E9')
		self.assertEqual(entry1.protein_existence_type, 'ET')
		self.assertEqual(entry1.ec, '5.3.3.1')
		entry2 = entries[1]
		self.assertEqual(entry2.db_id.db_id, 'Q197E9')
		self.assertEqual(entry2.protein_existence_type, 'ET')
		self.assertEqual(entry2.ec, '1.1.1.145')

	def test_ecs_parse_past_the_end(self):
		self.parser.next_ecs_entry()
		self.parser.next_ecs_entry()
		entry = self.parser.next_ecs_entry()
		self.assertEqual(entry, None)

	def test_run_ecs_parser(self):
		EcsEntry.objects.all().delete()
		uniprot_ecs_parser.run(["argv0", TEST_FILE_PATH + "test_uniprot.ecs"])
		entry = EcsEntry.objects.all()[0]
		self.assertEqual(entry.db_id.db_id, 'Q197F8')
		self.assertEqual(entry.protein_existence_type, 'P')
		self.assertEqual(entry.ec, '?')
