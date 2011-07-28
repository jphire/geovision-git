import sys
import geovision.text_to_db.db_parser
from geovision.text_to_db.bulk_inserter import BulkInserter
from geovision.viz.models import DbEntry

def run(args):
	try:
		parser = geovision.text_to_db.db_parser.DbfileParser(args[1], args[2])
	except IOError:
		print("Unable to open file", args[1])
		sys.exit(1);
	inserter = BulkInserter(DbEntry)
	db_entry = parser.next_db_entry()
	while db_entry is not None:
		inserter.save(db_entry)
		db_entry = parser.next_db_entry()
	inserter.close()

if __name__ == "__main__":
	run(sys.argv)
