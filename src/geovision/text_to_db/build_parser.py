from geovision.viz.models import Result, Read, DbEntry
from geovision.text_to_db.bulk_inserter import BulkInserter

def parseBuilds(sample_name, db_name, filehandle):
	"""Parse build data from a .build file and store it to the db.
		sample_name: name of the sample (eg. OLKR49)
		db_name: name of the database (eg. frnadb)
		filehandle: file handle of the data file
	"""
	inserter = BulkInserter(Result)
	for line in filehandle:
		(read_id, db_seq_id, evident_type, ec_number, error_value, bitscore) = line.strip().split("\t")
		db_entry = None		
		try:
			db_entry = DbEntry.objects.get(read_id__startswith=('sp|' + db_seq_id), source_file=db_name)
		except Exception as e:
			print (db_seq_id, db_name)
		read = Read.objects.get(read_id=read_id, sample=sample_name)

		inserter.save(Result(read=read, db_entry=db_entry, evident_type=evident_type, ec_number=ec_number,
			error_value=error_value, bitscore=bitscore))
	inserter.close()

if __name__ == '__main__':
	import sys
	filename = sys.argv[1]
	(sample_name, db_name, rest) = filename.split('.')
	parseBuilds(sample_name, db_name, open(filename, 'r'))
	
