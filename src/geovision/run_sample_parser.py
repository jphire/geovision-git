#coding: UTF-8
#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="lassetyr"
__date__ ="$30.5.2011 15:14:55$"

import sys
import geovision.text_to_db.sample_parser
from geovision.text_to_db.bulk_inserter import BulkInserter
from geovision.viz.models import Read

if __name__ == "__main__":
	try:
		parser = geovision.text_to_db.sample_parser.SamplefileParser(sys.argv[1])
	except IOError:
		print "Unable to open file", sys.argv[1]
		sys.exit(1);
	inserter = BulkInserter(Read, use_dict=True)
	read_entry = parser.next_read()
	while read_entry is not None:
		inserter.save(read_entry)
		read_entry = parser.next_read()
	inserter.close()
