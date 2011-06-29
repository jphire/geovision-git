from geovision.text_to_db.enzyme_list_parser import enzyme_parser, run
from viz.models import EnzymeName
from settings import TEST_FILE_PATH
import unittest
from nose.tools import eq_

from StringIO import StringIO

test1 = """FOO         bar;
            baz;
            biff
BAR         quux
BAZ         wtf
///
FOO         abc
BAR         xyz
///"""

class EnzymeParserTests(unittest.TestCase):
	parser = enzyme_parser(StringIO(test1), ['FOO', 'BAR'])

	def test_get_entry(self):
		eq_(self.parser.get_entry(), {'FOO': ['bar', 'baz', 'biff'], 'BAR': ['quux']})
		eq_(self.parser.get_entry(), {'FOO': ['abc'], 'BAR': ['xyz']})
		eq_(self.parser.get_entry(), None)
	def test_split(self):
		eq_(enzyme_parser.split('KEY         value;\n'), ('KEY', 'value'))
	def test_run_enzymeparser(self):
		EnzymeName.objects.all().delete()
		run(['argv0', TEST_FILE_PATH + 'enzyme_test.txt'])
		enames = EnzymeName.objects.all()
		eq_(len(enames), 27)
		eq_(enames[0].ec_number, '1.1.1.1')
		eq_(enames[0].enzyme_name, 'alcohol dehydrogenase')
		eq_(enames[11].ec_number, '1.1.1.1')
		eq_(enames[11].enzyme_name, 'yeast alcohol dehydrogenase')
		eq_(enames[26].ec_number, '1.1.1.3')
		eq_(enames[26].enzyme_name, 'HSD')