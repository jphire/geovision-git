import sys
import geovision.text_to_db.db_parser
from geovision.text_to_db.bulk_inserter import BulkInserter
from geovision.viz.models import DbEntry
from geovision.userdb import ImportedData

def run(args):
	try:
		parser = geovision.text_to_db.db_parser.DbfileParser(args[1], args[2])
	except IOError:
		print("Unable to open file", args[1])
		sys.exit(1);
	if ImportedData.objects.filter(type='dbentry', data=parser.source).exists()
		print("Warning: Not importing sample %s because it already exists")
		sys.exit(1)
	try:
		inserter = BulkInserter(DbEntry)
		db_entry = parser.next_db_entry()
		while db_entry is not None:
			inserter.save(db_entry)
			db_entry = parser.next_db_entry()
		inserter.close()
		ImpotedData.objects.create(type='dbentry', data=parser.source)
	except Exception as e:
		inserter.rollback()
		raise
if __name__ == "__main__":
	run(sys.argv)
