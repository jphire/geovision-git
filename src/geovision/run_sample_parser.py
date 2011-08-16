#coding: UTF-8
import sys
import geovision.text_to_db.sample_parser
from geovision.text_to_db.bulk_inserter import BulkInserter
from geovision.userdb import ImportedData
from geovision.viz.models import Read

def run(args):
	try:
		parser = geovision.text_to_db.sample_parser.SamplefileParser(args[1])
	except IOError:
		print "Unable to open file", args[1]
		sys.exit(1);
	if ImportedData.objects.filter(type='sample', data=parser.sample).exists()
		print("Warning: Not importing sample %s because it already exists")
		sys.exit(1)
	try:
		inserter = BulkInserter(Read)
		read_entry = parser.next_read()
		while read_entry is not None:
			inserter.save(read_entry)
			read_entry = parser.next_read()
		inserter.close()
		ImportedData.objects.create(type='sample', data=parser.sample)
	except Exception as e:
		inserter.rollback()
		raise 

if __nam__ == "__main__":
	run(sys.argv)
