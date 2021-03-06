from decimal import *
from django.utils import unittest

from geovision.settings import TEST_FILE_PATH, RUNNING_ON_USERS
from geovision.text_to_db.blast_parser import create_blast
from geovision.viz.models import Blast, BlastExtra
from geovision.viz.models import DbEntry
from geovision.viz.models import Read
from nose.tools import raises

@unittest.skipUnless(RUNNING_ON_USERS, "Blast parser tests require a PostgreSQL database")
class BlastParserTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		if not RUNNING_ON_USERS:
			return
		#in case objects left from other tests..
		DbEntry.objects.all().delete()
		Read.objects.all().delete()

		file = open(TEST_FILE_PATH + "test_blast.txt")	
		cls.read = Read.objects.create(sample="ABLU", read_id="gi|185682811|gb|ABLU01132423.1|", description="baz", data='ASD')
		cls.strings = []
		#creating db_entrys for all lines in test file
		for line in file:
			cls.str = line.split(None)
			cls.strings.append(cls.str)
			DbEntry.objects.create(source_file="uniprot", db_id=cls.str[1].split('|')[1], description="quux", data='ASD')

		cls.dbe = DbEntry.objects.all()
		create_blast(cls.dbe[0].source_file, cls.read.sample, TEST_FILE_PATH + "test_blast.txt")

	def test_parse_blast(self):
		

		results = Blast.objects.all()
		extras = BlastExtra.objects.all()
		self.assertEqual(len(results), len(extras))
		for i in range(len(results)):
			self.assertEqual(results[i].read, self.read)
			self.assertEqual(results[i].database_name, self.dbe[i].source_file)
			self.assertEqual(results[i].db_entry, self.dbe[i])
			self.assertEqual(str(results[i].error_value), self.strings[i][10])
			self.assertEqual(results[i].bitscore, float(self.strings[i][11]))

			self.assertEqual(extras[i].pident, float(self.strings[i][2]))
			self.assertEqual(extras[i].length, Decimal(self.strings[i][3]))
			self.assertEqual(extras[i].mismatch, Decimal(self.strings[i][4]))
			self.assertEqual(extras[i].gapopen, Decimal(self.strings[i][5]))
			self.assertEqual(extras[i].qstart, Decimal(self.strings[i][6]))
			self.assertEqual(extras[i].qend, Decimal(self.strings[i][7]))
			self.assertEqual(extras[i].sstart, Decimal(self.strings[i][8]))
			self.assertEqual(extras[i].send, Decimal(self.strings[i][9]))


#	@raises(Read.DoesNotExist)
#	def testNonexistentRead(self):
#		create_blast('SMPL', 'FOODB', TEST_FILE_PATH + "test_blast.txt")

#	@raises(DbEntry.DoesNotExist)
#	def testNonexistentDbEntry(self):
#		create_blast('SMPL', 'FOODB', TEST_FILE_PATH + "test_blast.txt")

if __name__ == '__main__':
	unittest.main()

