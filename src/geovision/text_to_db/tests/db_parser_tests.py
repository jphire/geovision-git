#coding: UTF-8
import unittest
import text_to_db.db_parser as db_parser

from geovision.settings import TEST_FILE_PATH
from viz.models import DbEntry

class DbParserTests(unittest.TestCase):
	def test_db_parse_first_uniprot(self):
		parser = db_parser.DbfileParser(TEST_FILE_PATH + "db_test_uniprot.fasta")
		entry = parser.next_db_entry()
		self.assertEqual(entry.db_id, 'Q197F8')
		self.assertEqual(entry.source_file, 'db_test_uniprot')
		self.assertEqual(entry.sub_db, 'sp')
		self.assertEqual(entry.entry_name, '002R_IIV3')
		self.assertEqual(entry.description, 'Uncharacterized protein 002R')
		self.assertEqual(entry.os_field, 'Invertebrate iridescent virus 3')
		self.assertEqual(entry.other_info, 'GN=IIV3-002R PE=4 SV=1')
		self.assertEqual(entry.data, "MASNTVSAQGGSNRPVRDFSNIQDVAQFLLFDPIWNEQPGSIVPWKMNREQALAERYPEL\
QTSEPSEDYSGPVESLELLPLEIKLDIMQYLSWEQISWCKHPWLWTRWYKDNVVRVSAIT\
FEDFQREYAFPEKIQEIHFTDTRAEEIKAILETTPNVTRLVIRRIDDMNYNTHGDLGLDD\
LEFLTHLMVEDACGFTDFWAPSLTHLTIKNLDMHPRWFGPVMDGIKSMQSTLKYLYIFET\
YGVNKPFVQWCTDNIETFYCTNSYRYENVPRPIYVWVLFQEDEWHGYRVEDNKFHRRYMY\
STILHKRDTDWVENNPLKTPAQVEMYKFLLRISQLNRDGTGYESDSDPENEHFDDESFSS\
GEEDSSDEDDPTWAPDSDDSDWETETEEEPSVAARILEKGKLTITNLMKSLGFKPKPKKI\
QSIDRYFCSLDSNYNSEDEDFEYDSDSEDDDSDSEDDC")

	def test_db_parse_second_uniprot(self):
		parser = db_parser.DbfileParser(TEST_FILE_PATH + "db_test_uniprot.fasta")
		parser.next_db_entry()
		entry = parser.next_db_entry()
		self.assertEqual(entry.db_id, 'Q197F7')
		self.assertEqual(entry.source_file, 'db_test_uniprot')
		self.assertEqual(entry.sub_db, 'sp')
		self.assertEqual(entry.entry_name, '003L_IIV3')
		self.assertEqual(entry.description, 'Uncharacterized protein 003L')
		self.assertEqual(entry.os_field, 'Invertebrate iridescent virus 3')
		self.assertEqual(entry.other_info, 'GN=IIV3-003L PE=4 SV=1')
		self.assertEqual(entry.data, "MYQAINPCPQSWYGSPQLEREIVCKMSGAPHYPNYYPVHPNALGGAWFDTSLNARSLTTT\
PSLTTCTPPSLAACTPPTSLGMVDSPPHINPPRRIGTLCFDFGSAKSPQRCECVASDRPS\
TTSNTAPDTYRLLITNSKTRKNNYGTCRLEPLTYGI")

	def test_db_parse_past_the_end_uniprot(self):
		parser = db_parser.DbfileParser(TEST_FILE_PATH + "db_test_uniprot.fasta")
		for i in xrange(0,10):
			parser.next_db_entry()
		entry = parser.next_db_entry()
		self.assertEqual(entry, None)


	def test_db_parse_first_silva_ssu(self):
		parser = db_parser.DbfileParser(TEST_FILE_PATH + "db_test_silva_ssu.fasta")
		entry = parser.next_db_entry()
		self.assertEqual(entry.db_id, 'A93610.1.1301')
		self.assertEqual(entry.source_file, 'db_test_silva_ssu')
		self.assertEqual(entry.description, 'Archaea;Euryarchaeota;Thermococci;Thermococcales;Thermococcaceae;Thermococcus;unidentified')
		self.assertEqual(entry.os_field, '')
		self.assertEqual(entry.other_info, '')
		self.assertEqual(entry.data, "CCACUGCUAUGGGGGUCCGACUAAGCCAUGCGAGUCAUGGGGUCCCUCUGGGACACCACCG\
GCGGACGGCUCAGUAACACGUCGGUAACCUACCCUCGGGAGGGGGAUAACCCCGGGAAACUGGGGCUAAUCCCCCAUAGGCCUGAGGUACUGGAAGGUCC\
UCAGGCCGAAAGGGGCUUUUGCCCGCCCGAGGAUGGGCCGGCGGCCGAUUAGGUAGUUGGUGGGGUAACGGCCCACCAAGCCGAAGAUCGGUACGGGCUG\
UGAGAGCAGGAGCCCGGAGAUGGACACUGAGACACGGGUCCAGGCCCUACGGGGCGCAGCAGGCGCGAAACCUCCGCAAUGCGGGAAACCGCGACGGGGG\
GACCCCGAGUGCCGUGGUAUCGACACGGUUUUUCCGGAGUGUAAAAAGCUCCGGGAAUAAGGGCUGGNCAAGGCCGGUGGCAGCCGCCGCGGUAAUACCG\
GCGGCCCGAGUGGUGGCCGCUAUUAUUGGGCCUAAAGCGUCCGUAGCCGGGCCCGUAAGUCCCUGGCGAAAUCCCACGGCUCAACCGUGGGGCUUGCUGG\
GGAUACUGCGGGCCUUGGGACCGGGAGAGGCCGGGGGUACCCCUGGGGUAGGGGUGAAAUCCUAUAAUCCCAGGGGGACCGCCAGUGGCGAAGGCGCCCG\
GCUGGAACGGGUCCGACGGUGAGGGACGAAGGCCAGGGGAGCAAACCGGAUUAGAUACCCGGGUAGUCCUGGAUGUAAAGGAUGCGGGCUAGGUGUCGGG\
CGAGCUUCGAGCUCGCCCGGUGCCGUAGGGAAGCCGUUAAGCCCGCCGCCUGGGGAGUACGGCCGCAAGGCUGAAACUUAAAGGAAUUGNCGGGGGAGCA\
CUACAAGGGGUGGAGCGUGCGGUUUAAUUGGAUUCAACGCCGGGAACCUCACCGGGGGCGACGGCAGGAUGAAGGCCAGGCUGAAGGUCUUGCCGGACAC\
GCCGAGAGGAGGUGCAUGGCCGCCGUCAGCUCGUACCGUGAGGCGUCCACUUAAGUGUGGUAACGAGCGAGACCCGCGCCCCCAGUUGCCAGCCCUUCCC\
GUUGGGAAGGGGGCACUCUGGGGGGACUGCCGGCGAUAAGCCGGAGGAAGGAGCGGGCGACGGUAGGUCAGUAUGCCCCGAAACCCCCGGGCUACACGCG\
CGCUACAAUGGGCGGGACAAUGGGAUCCGACCCCGAAAGGGGAAGGUAAUCCCCUAAACCCGCCCUCAGUUCGGAUCGCGGGCUGCAACUCGCCCGCGUG\
AAGCUGGAAUCCCUAGUACCCGCGUGUCAUCAUCGCGCGG")

	def test_db_parse_second_silva_ssu(self):
		parser = db_parser.DbfileParser(TEST_FILE_PATH + "db_test_silva_ssu.fasta")
		parser.next_db_entry()
		entry = parser.next_db_entry()
		self.assertEqual(entry.db_id, 'AAAA02014925.13286.14671')
		self.assertEqual(entry.description, 'Bacteria;Proteobacteria;Alphaproteobacteria;Rickettsiales;mitochondria;Oryza sativa Indica Group')
		self.assertEqual(entry.os_field, '')
		self.assertEqual(entry.other_info, '')
		self.assertEqual(entry.data, "UCUGAGUUUGAUCCUGGCUCAGAAGGAACGCUAGCUAUAUGCUUAACAUAUGCAAGUCGAA\
CGUUGUUUUCGGGGAGCUGGGCAGAAGGAAAAGAGGCUCCUAGCUAAAGUAGUCUCGCCCUGCUUCAAAACUACAGGGCG\
CGCGCUACGGCUUUGACCUAACGGCCUCCGUUUGCUGGAAUCGGAAUAGUUGAGAACAAAGUGGCGAACGGGUGCGUAACGCGUGGGAAUCUGCUGAAC\
AGUUCGGGCCAAAUCCUGAAGAAAGCUCAAAAGCGUUGUUUGAUGAGCCUGCGUAGUAUUAGGUAGUUGGUCGGGUAAAGGCUGACCAAGCCAAUGAUG\
CUUAGCUGGUCUUUUCGGAUGAUCAGCCACACUGGGAUUGAGACACGGCCCAGACUCCCACGGGGGGCAGCAGUGGGGAAUCUUGGACAAUGGGCGAAA\
GCCUAAUCCAGCAAUAUCGCGUGAGUGAAGAAGGGCAAUGCCGCUUGUAAAGCUCUUUCGUCGAGUGCGCGAUCAUGACAGGACUCGAGGAAGAAGCCC\
CGGCUAACUCCGUGCCAGCAGCCGCGGUAAGACGGGAGGGGGGGGCAAGUGUUCUUCGGAAUGACUAGGCGUAAAGGGCACGUAGGCGGUGACAUCGGG\
UUGAAAGUGAAAGUCGCCCAAAAAGUGCCGGAAUGCUCUCGAAACCAAUUCACUUGAGUGAGACAGAGGAGAGUGGAAUUUCGUGUGUAGGGGUGAAAU\
CCGUAGAUCUACGAAGGAACGCCAAAAGCGAAGGCAGCUCUCUGGGUCCCUACCGACGCUGGGGUGCGAAAGCAUGGGGAGCGAACAGGAUUAGAUACC\
CUGGUAGUCUAUGCUGUAAACGAUGAGUGUUCGCCCUUGGUCUACGCGGAUCAGGGGCCCAGCUAACGCGUGAAACACUCCGCCUGGGGAGUACGGUCG\
CAAGACCGAAACUCAAAGGAAUUGACGGGGGCCUGCACAAGCGGUGGAGCAUGUGGUUUAAUUCAAUACAAUGCGCAAAACCUUUGUCACACCCUAAAA\
AUCCCAAAUAUAUAAAUUGUUGUCUAAAUUGGAAUUAUUAGAAUUUAUUUUAAAAGCCUAGAAGAGAAAAUCUAGUUUUAAUUAAUAAAUUCCAAUAUA\
AAAUGGGGCCAGAUAAAAUUUCAUUAAAUACUUUGCUUGAUUCUAUAGUUCCUAGAGUUUUCUGGGAUUUAUUUGAGCCAAGGAAGUAUUUUUAAUAAA\
UGGAAUUGCAUUUCAUGAAUAAUUUAAAUUGAAAAAGGUUUUUUAAAAGUCUCUUUGGCUUUGGGCCGAAAGUCGGCCCAAAACCCUCUCUCUCUCCUC\
CUCGGCCCAAGUCAGCCCAAGUCAAGCCGAGCCGCGCGCGCGCUCGCUGCUGUUGAC")

	def test_db_parse_past_the_end_silva_ssu(self):
		parser = db_parser.DbfileParser(TEST_FILE_PATH + "db_test_silva_ssu.fasta")
		for i in xrange(0,3):
			parser.next_db_entry()
		entry = parser.next_db_entry()
		self.assertEqual(entry, None)

	def test_db_parse_first_frnadb(self):
		parser = db_parser.DbfileParser(TEST_FILE_PATH + "db_test_frnadb.fasta")
		entry = parser.next_db_entry()
		self.assertEqual(entry.db_id, 'FR000001')
		self.assertEqual(entry.source_file, 'db_test_frnadb')
		self.assertEqual(entry.description, 'AB027356;Group II intron')
		self.assertEqual(entry.os_field, '')
		self.assertEqual(entry.other_info, '')
		self.assertEqual(entry.data, "TTGAGCCGTATGCGATGAAAGTTGCACGTACGGTTCTTTAAGGGGGAAAGTTTGAGAGGACCTACCTATCTTAAC")

	def test_db_parse_second_frnadb(self):
		parser = db_parser.DbfileParser(TEST_FILE_PATH + "db_test_frnadb.fasta")
		parser.next_db_entry()
		entry = parser.next_db_entry()
		self.assertEqual(entry.db_id, 'FR000002')
		self.assertEqual(entry.description, 'AJ001501;5.8S ribosomal RNA (rRNA)')
		self.assertEqual(entry.os_field, '')
		self.assertEqual(entry.other_info, '')
		self.assertEqual(entry.data, "AAATCTTAGCGGTGGATCACTCGGTTCGTGGATCGATGAAGAACGCAGCTAGCTGCGATAAATAGTGCGA\
ATTGCAGACACATTGAGCACTAAAAATTCGAACGTACATTGCGCCATCGGGTTCATTCCCGTTGGCACGTCTGGCTGAGGGTTG")

	def test_db_parse_past_the_end_frnadb(self):
		parser = db_parser.DbfileParser(TEST_FILE_PATH + "db_test_frnadb.fasta")
		for _ in xrange(0,3):
			parser.next_db_entry()
		entry = parser.next_db_entry()
		self.assertEqual(entry, None)

	def test_run_db_parser(self):
		import run_db_parser
		DbEntry.objects.all().delete()

		run_db_parser.run(["argv0", TEST_FILE_PATH + "db_test_frnadb.fasta", 'db_test_frnadb'])
		entrys = DbEntry.objects.all()
		self.assertEqual(len(entrys), 2)
		entry = entrys[0]
		self.assertEqual(entry.db_id, 'FR000001')
		self.assertEqual(entry.source_file, 'db_test_frnadb')
		self.assertEqual(entry.description, 'AB027356;Group II intron')
		self.assertEqual(entry.os_field, '')
		self.assertEqual(entry.other_info, '')
		self.assertEqual(entry.data, "TTGAGCCGTATGCGATGAAAGTTGCACGTACGGTTCTTTAAGGGGGAAAGTTTGAGAGGACCTACCTATCTTAAC")
