#coding: UTF-8
#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="lassetyr"
__date__ ="$14.6.2011 18:03:24$"

import sys
import geovision.text_to_db.sample_parser
from geovision.text_to_db.bulk_inserter import BulkInserter
from geovision.viz.models import DbEntry

if __name__ == "__main__":
	try:
		parser = geovision.text_to_db.db_parser.SamplefileParser(sys.argv[1], sys.argv[2])
	except IOError:
		print "Unable to open file", argv[1]
		sys.exit(1);
	inserter = BulkInserter(DbEntry)
	entry = parser.next()
	while entry is not None:
		inserter.save(entry)
		entry = parser.next()
	inserter.close()