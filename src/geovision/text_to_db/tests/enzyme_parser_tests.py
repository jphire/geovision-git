from geovision.text_to_db.enzyme_list_parser import enzyme_parser
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

class enzyme_parser_tests(unittest.TestCase):
	parser = enzyme_parser(StringIO(test1), ['FOO', 'BAR'])

	def test_get_entry(self):
		eq_(self.parser.get_entry(), {'FOO': ['bar', 'baz', 'biff'], 'BAR': ['quux']})
		eq_(self.parser.get_entry(), {'FOO': ['abc'], 'BAR': ['xyz']})
		eq_(self.parser.get_entry(), None)
	def test_split(self):
		eq_(enzyme_parser.split('KEY         value;\n'), ('KEY', 'value'))
