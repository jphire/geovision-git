#coding: UTF-8
#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="lassetyr"
__date__ ="$30.5.2011 15:14:55$"

import sys
import geovision.text_to_db.sample_parser

if __name__ == "__main__":
	try:
		parser = geovision.text_to_db.sample_parser.SamplefileParser(sys.argv[1])
	except IOError:
		print "Unable to open file", argv[1]
		sys.exit(1);
	db_read_entry = parser.next_read()
	while db_read_entry is not None:
		print db_read_entry.read_id
		db_read_entry.save()