# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="lassetyr"
__date__ ="$17.6.2011 14:15:47$"

import sys
import geovision.text_to_db.db_parser
from geovision.text_to_db.bulk_inserter import BulkInserter
from geovision.viz.models import DbEntry

if __name__ == "__main__":
	try:
		parser = geovision.text_to_db.db_parser.DbfileParser(sys.argv[1], sys.argv[2])
	except IOError:
		print("Unable to open file", sys.argv[1])
		sys.exit(1);
	inserter = BulkInserter(DbEntry)
	db_entry = parser.next_db_entry()
	while db_entry is not None:
		inserter.save(db_entry)
		db_entry = parser.next_db_entry()
	inserter.close()
