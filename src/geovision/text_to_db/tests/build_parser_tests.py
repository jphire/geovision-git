from django.test import TestCase
from geovision.text_to_db.build_parser import parseBuilds
from viz.models import *
from StringIO import StringIO
from nose.tools import eq_

class BuildParserTestsTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.read = Read.objects.create(sample="SMPL", read_id="R001", description="baz", data='ASD')
		cls.dbe1 = DbEntry.objects.create(source_file="FOODB", db_id="DB002", description="quux", data='ASD')
		cls.dbe2 = DbEntry.objects.create(source_file="FOODB", db_id="DB042", description="biff", data='AOE')

	def testSuccesfulBuilds(self):

		Result.objects.all().delete()
		errors = parseBuilds('SMPL', 'FOODB', StringIO(
		"""R001\tDB002\tH\t4.-.-.-\t0.049\t36.6\n""" +
		"""asdasdasd\n""" +
		"""R001\tDB042\tH\t3.5.4.n1\t0.017\t38.1\n"""))
		eq_(errors, ['asdasdasd\n'])
		results = Result.objects.all()
		eq_(len(results), 2)
		res1 = results[0]
		eq_(res1.read,self.read.read_id)
		eq_(res1.db_entry, self.dbe1.db_id)
		eq_(res1.evident_type, 'H')
		eq_(res1.ec_number, '4.-.-.-')
		eq_(res1.error_value, 0.049)
		eq_(res1.bitscore, 36.6)

#	@raises(Read.DoesNotExist)
#	def testNonexistentRead(self):
#		parseBuilds('SMPL', 'FOODB', StringIO("""ASDSDSDSADSADASADSDA\tDB002\tH\t4.-.-.-\t0.049\t36.6\n"""))
#
#	@raises(DbEntry.DoesNotExist)
#	def testNonexistentDbEntry(self):
#		parseBuilds('SMPL', 'FOODB', StringIO("""R001\tDB_ASDSADSADSA\tH\t4.-.-.-\t0.049\t36.6\n"""))
