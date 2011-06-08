# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from geovision.text_to_db.create_JSON import *
from geovision.viz.models import Result, Read, DbEntry, Blast

class  Test_create_JSONTestCase(unittest.TestCase):
    def setUp(self):

        Read.objects.create(sample="SMPL1", read_id="R001", description="baz", data='ASD')
        Read.objects.create(sample="SMPL2", read_id="R002", description="baz", data='ASD')
        Read.objects.create(sample="SMPL3", read_id="R003", description="baz", data='ASD')
        Read.objects.create(sample="SMPL4", read_id="R004", description="baz", data='ASD')
        Read.objects.create(sample="SMPL3", read_id="R005", description="baz", data='ASD')
        Read.objects.create(sample="SMPL2", read_id="R006", description="baz", data='ASD')

        DbEntry.objects.create(source_file = "uniprot", read_id = "DB1", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", read_id = "DB2", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", read_id = "DB3", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", read_id = "DB4", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", read_id = "DB5", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", read_id = "DB6", description="quux", data='ASD')
        DbEntry.objects.create(source_file = "uniprot", read_id = "DB7", description="quux", data='ASD')

        read1 = Read.objects.get(read_id="R001")
        read2 = Read.objects.get(read_id="R002")
        read3 = Read.objects.get(read_id="R003")
        read4 = Read.objects.get(read_id="R004")
        read5 = Read.objects.get(read_id="R005")
        read6 = Read.objects.get(read_id="R006")

        db_entry1= DbEntry.objects.get(read_id="DB1")
        db_entry2= DbEntry.objects.get(read_id="DB2")
        db_entry3= DbEntry.objects.get(read_id="DB3")
        db_entry4= DbEntry.objects.get(read_id="DB4")
        db_entry5= DbEntry.objects.get(read_id="DB5")
        db_entry6= DbEntry.objects.get(read_id="DB6")
        db_entry7= DbEntry.objects.get(read_id="DB7")

        Result.objects.create(read=read1, db_entry=db_entry1, evident_type="l", ec_number="1.1.2.22",
			error_value=0.002, bitscore=50)
        Result.objects.create(read=read2, db_entry=db_entry1, evident_type="l", ec_number="1.1.2.22",
			error_value=0.002, bitscore=30)
        Result.objects.create(read=read3, db_entry=db_entry2, evident_type="l", ec_number="1.1.2.22",
			error_value=0.002, bitscore=50)
        Result.objects.create(read=read5, db_entry=db_entry4, evident_type="l", ec_number="1.1.2.22",
			error_value=0.002, bitscore=30)
        Result.objects.create(read=read4, db_entry=db_entry6, evident_type="l", ec_number="1.1.2.22",
			error_value=0.002, bitscore=50)

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_create_JSON(self):

        print Read.objects.all().count()
        print DbEntry.objects.all().count()
        print Blast.objects.all().count()
        print Result.objects.all().count()

        create_json("1.1.2.22", 20, 4)

        assert 1==1
        #assert x != y;
        #self.assertEqual(x, y, "Msg");

if __name__ == '__main__':
    unittest.main()

