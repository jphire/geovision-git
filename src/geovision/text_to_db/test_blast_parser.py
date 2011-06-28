# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from decimal import *
from nose.tools import raises
from geovision.text_to_db.blast_parser import create_blast
from geovision.viz.models import Result, Read, DbEntry, Blast
from geovision.settings import TEST_FILE_PATH

class Test_blast_parserTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):

        file = open(TEST_FILE_PATH + "test_blast.txt")
        #in case objects left from other tests..
        DbEntry.objects.all().delete()
        Read.objects.all().delete()
        
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
#        print self.strings[1]
	results = Blast.objects.all()
	for i in range(len(results)):
		self.assertEqual(results[i].read, self.read)
		self.assertEqual(results[i].database_name, self.dbe[i].source_file)
		self.assertEqual(results[i].db_entry, self.dbe[i])
		self.assertEqual(results[i].pident, float(self.strings[i][2]))
		self.assertEqual(results[i].length, Decimal(self.strings[i][3]))
		self.assertEqual(results[i].mismatch, Decimal(self.strings[i][4]))
		self.assertEqual(results[i].gapopen, Decimal(self.strings[i][5]))
		self.assertEqual(results[i].qstart, Decimal(self.strings[i][6]))
		self.assertEqual(results[i].qend, Decimal(self.strings[i][7]))
		self.assertEqual(results[i].sstart, Decimal(self.strings[i][8]))
		self.assertEqual(results[i].send, Decimal(self.strings[i][9]))
		self.assertEqual(str(results[i].error_value), self.strings[i][10])
		self.assertEqual(results[i].bitscore, float(self.strings[i][11]))

#
#    @raises(Read.DoesNotExist)
#    def testNonexistentRead(self):
#            create_blast('SMPL', 'FOODB', "test_blast.txt")
#
#    @raises(DbEntry.DoesNotExist)
#    def testNonexistentDbEntry(self):
#            create_blast('SMPL', 'FOODB', "test_blast.txt")

if __name__ == '__main__':
    unittest.main()

