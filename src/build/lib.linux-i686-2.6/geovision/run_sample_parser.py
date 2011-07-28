#coding: UTF-8
import sys
import geovision.text_to_db.sample_parser
from geovision.text_to_db.bulk_inserter import BulkInserter
from geovision.viz.models import Read

def run(args):
	try:
		parser = geovision.text_to_db.sample_parser.SamplefileParser(args[1])
	except IOError:
		print "Unable to open file", args[1]
		sys.exit(1);
	inserter = BulkInserter(Read)
	read_entry = parser.next_read()
	while read_entry is not None:
		inserter.save(read_entry)
		read_entry = parser.next_read()
	inserter.close()
if __name__ == "__main__":
	run(sys.argv)