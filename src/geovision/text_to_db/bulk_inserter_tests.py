from geovision.text_to_db.models import BulkInserterTestDummy
import unittest
from nose.tools import *

from geovision.text_to_db.models import BulkInserterTestModel
from geovision.text_to_db.models import *
from geovision.text_to_db.bulk_inserter import BulkInserter

class BulkInserterTests(unittest.TestCase):
	def setUp(self):
		self.dummy_obj = BulkInserterTestDummy(id=27)
		self.obj = BulkInserterTestModel(int_field=42, char_field='Foo', fk_field=self.dummy_obj)
		self.obj2 = BulkInserterTestModel(int_field=421, char_field='Bar', fk_field=self.dummy_obj)

	def testObjToCsv(self):
		inserter = BulkInserter(BulkInserterTestModel)
		eq_(inserter.obj_to_csv(inserter, self.obj), "1$42$Foo$27\n")
		inserter.close()

	def testSave(self):
		self.dummy_obj.save()

		generic_inserter = BulkInserter(BulkInserterTestModel)
		generic_inserter.save(self.obj)
		generic_inserter.save(self.obj2)
		generic_inserter.close()

		tests = BulkInserterTestModel.objects.all()
		eq_(tests[0].int_field, self.obj.int_field)
		eq_(tests[0].char_field, self.obj.char_field)
		eq_(tests[0].fk_field, self.obj.fk_field)

		eq_(tests[1].int_field, self.obj2.int_field)
		eq_(tests[1].char_field, self.obj2.char_field)
		eq_(tests[1].fk_field, self.obj2.fk_field)

if __name__ == '__main__':
    unittest.main()
