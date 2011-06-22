# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from geovision.text_to_db.create_JSON import *
from geovision.viz.models import Result, Read, DbEntry, Blast

class  Test_create_JSONTestCase(unittest.TestCase):
    def setUp(self):

        Read.objects.create(sample="SMPL1", read_id="R1", description="baz", data='ASD')
        Read.objects.create(sample="SMPL2", read_id="R2", description="baz", data='ASD')
        Read.objects.create(sample="SMPL3", read_id="R3", description="baz", data='ASD')
        Read.objects.create(sample="SMPL4", read_id="R4", description="baz", data='ASD')
        Read.objects.create(sample="SMPL3", read_id="R5", description="baz", data='ASD')
        Read.objects.create(sample="SMPL2", read_id="R6", description="baz", data='ASD')

        DbEntry.objects.create(source_file = "uniprot", db_id = "DB1", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", db_id = "DB2", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", db_id = "DB3", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", db_id = "DB4", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", db_id = "DB5", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", db_id = "DB6", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", db_id = "DB7", description="quux", data='ASD')

        read1 = Read.objects.get(read_id="R1")
        read2 = Read.objects.get(read_id="R2")
        read3 = Read.objects.get(read_id="R3")
        read4 = Read.objects.get(read_id="R4")
        read5 = Read.objects.get(read_id="R5")
        read6 = Read.objects.get(read_id="R6")

        db_entry1= DbEntry.objects.get(db_id="DB1")
        db_entry2= DbEntry.objects.get(db_id="DB2")
        db_entry3= DbEntry.objects.get(db_id="DB3")
        db_entry4= DbEntry.objects.get(db_id="DB4")
        db_entry5= DbEntry.objects.get(db_id="DB5")
        db_entry6= DbEntry.objects.get(db_id="DB6")
        db_entry7= DbEntry.objects.get(db_id="DB7")

        Result.objects.create(read="R1", db_entry="DB1", evident_type="l", ec_number="1.1.2.22",
			error_value=0.005, bitscore=50)
        Result.objects.create(read="R2", db_entry="DB1", evident_type="l", ec_number="1.1.2.22",
			error_value=0.002, bitscore=30)
        Result.objects.create(read="R3", db_entry="DB2", evident_type="l", ec_number="1.1.2.22",
			error_value=0.005, bitscore=50)
        Result.objects.create(read="R5", db_entry="DB4", evident_type="l", ec_number="1.1.2.24",
			error_value=0.002, bitscore=30)
        Result.objects.create(read="R4", db_entry="DB6", evident_type="l", ec_number="1.1.2.22",
			error_value=0.002, bitscore=780)
        Result.objects.create(read="R1", db_entry="DB2", evident_type="l", ec_number="1.1.2.22",
			error_value=0.002, bitscore=70)
        Result.objects.create(read="R1", db_entry="DB2", evident_type="l", ec_number="1.1.2.24",
			error_value=0.004, bitscore=50)
        Result.objects.create(read="R1", db_entry="DB3", evident_type="l", ec_number="1.1.2.23",
			error_value=0.002, bitscore=100)
        Result.objects.create(read="R2", db_entry="DB5", evident_type="l", ec_number="1.1.2.24",
			error_value=0.001, bitscore=90)


        Result.objects.create(read="R4", db_entry="DB6", evident_type="l", ec_number="1.1.2.22",
			error_value=0.002, bitscore=50)
        Result.objects.create(read="R1", db_entry="DB2", evident_type="l", ec_number="1.1.2.22",
			error_value=0.003, bitscore=70)
        Result.objects.create(read="R1", db_entry="DB2", evident_type="l", ec_number="1.1.2.24",
			error_value=0.002, bitscore=33)
        Result.objects.create(read="R1", db_entry="DB3", evident_type="l", ec_number="1.1.2.23",
			error_value=0.003, bitscore=44)
        Result.objects.create(read="R1", db_entry="DB4", evident_type="l", ec_number="1.1.2.24",
			error_value=0.002, bitscore=55)

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_create_JSON(self):

        print Read.objects.all().count()
        print DbEntry.objects.all().count()
        print Blast.objects.all().count()
        print Result.objects.all().count()

        create_json('1.1.2.22', 0, 0, 20, 0.006, 2, 5)

        assert 1==1
        #assert x != y;
        #self.assertEqual(x, y, "Msg");

if __name__ == '__main__':
    unittest.main()

