from geovision.text_to_db.models import BulkInserterTestDummy
import unittest
from nose.tools import *

from geovision.text_to_db.models import BulkInserterTestModel
from geovision.text_to_db.models import *
from geovision.text_to_db.bulk_inserter import BulkInserter

class BulkInserterTests(unittest.TestCase):
	def setUp(self):
		self.inserter = BulkInserter(BulkInserterTestModel)
		self.dummy_obj = BulkInserterTestDummy(id=27)
		self.obj = BulkInserterTestModel(int_field=42, char_field='Foo', fk_field=self.dummy_obj)

	def testObjToCsv(self):
		eq_(self.inserter.obj_to_csv(self.obj, 18), '18^42^Foo^27')

	def testGenericSave(self):
		generic_inserter = BulkInserter(BulkInserterTestModel)
		generic_inserter.save(self.obj)
		generic_inserter.close()
		eq_(BulkInserterTestModel.objects.all()[0], self.obj)

if __name__ == '__main__':
    unittest.main()
