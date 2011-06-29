from geovision.viz.models import Result, Read, DbEntry
from geovision.text_to_db.bulk_inserter import BulkInserter

import os

DEBUG = False

def parseBuilds(sample_name, db_name, filehandle):
	"""Parse build data from a .build file and store it to the db.
		sample_name: name of the sample (eg. OLKR49)
		db_name: name of the database (eg. frnadb)
		filehandle: file handle of the data file
	"""
	errors = []
	inserter = BulkInserter(Result)
	for line in filehandle:
		try:
			(read_id, db_seq_id, evident_type, ec_number, error_value, bitscore) = line.strip().split("\t")
		except ValueError:
			errors += [line]
			continue

		inserter.save(Result(read=read_id, db_entry=db_seq_id, evident_type=evident_type, ec_number=ec_number,
			error_value=error_value, bitscore=bitscore))
	inserter.close()
	return errors

if __name__ == '__main__':
	import sys
	filename = sys.argv[1]
	(sample_name, db_name, extension) = os.path.basename(filename).split('.')
	errs = parseBuilds(sample_name, db_name, open(filename, 'r'))
	for err in errs:
		print "Warning, incorrectly formatted line: " + err