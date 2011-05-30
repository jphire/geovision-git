from geovision.viz.models import Result, Read, DbEntry

def parseBuilds(sample_name, db_name, filehandle):
	"""Parse build data from a .build file and store it to the db.
		sample_name: name of the sample (eg. OLKR49)
		db_name: name of the database (eg. frnadb)
		filehandle: file handle of the data file
	"""
	for line in filehandle:
		(read_id, db_seq_id, evident_type, ec_number, error_value, bitscore) = line.split("\t")
		db_entry = DbEntry.objects.get(read_id=db_seq_id, source_file=db_name)
		read = Read.objects.get(read_id=read_id, sample=sample_name)

		Result.objects.create(read=read, db_entry=db_entry, evident_type=evident_type, ec_number=ec_number,
			error_value=error_value, bitscore=bitscore)

if __name__ == '__main__':
	import sys
	filename = sys.argv[1]
	(sample_name, db_name) = filename.split('.')
	parse_blast(sample_name, db_name, open(filename, 'r'))