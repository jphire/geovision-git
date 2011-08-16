#coding: UTF-8

import os
from geovision.viz.models import Blast, BlastExtra
from geovision.viz.models import Read, DbEntry, ImportedData
from geovision.text_to_db.bulk_inserter import BulkInserter, dict_from_kwargs

inserter = BulkInserter(Blast, use_dict=True)
extra_inserter = BulkInserter(BlastExtra, use_dict=True)
def create_blast(db_name, sample_name, filename):
	global inserter, extra_inserter
	filehandle = open(filename, 'r')

	for line in filehandle:
		(read_id, db_seq_id, pident, length, mismatch, gapopen, qstart, qend, sstart, send, error_value, bitscore, read_seq, db_seq) = line.split(None)
		if db_name == 'uniprot':
			db_seq_id = db_seq_id.split('|')[1]
		id = inserter.get_id()
		inserter.save(dict_from_kwargs(read_id=read_id, database_name=db_name, sample=sample_name, db_entry_id=db_seq_id, bitscore=bitscore, error_value=error_value))
		extra_inserter.save(dict_from_kwargs(blast_id=id, pident=pident, length=length, mismatch=mismatch, gapopen=gapopen, qstart=qstart, qend=qend, sstart=sstart, send=send, read_seq=read_seq, db_seq=db_seq))
	inserter.close()
	extra_inserter.close()
	
if __name__ == '__main__':
	import sys
	filename = sys.argv[1]
	(sample_name, db_name, rest) = os.path.basename(filename).split('.')
	blast_name = sample_name + '.' + db_name
	if ImportedData.objects.filter(type='blast', data=blast_name).exists():
		print("Not importing blast %s because it already exists" % blast_name)
		sys.exit(1)
	if not ImportedData.objects.filter(type='sample', data=sample_name).exists():
		print("Not importing blast %s because sample %s doesn't exist" % (blast_name, sample_name)) 
		sys.exit(1)
	if not ImportedData.objects.filter(type='dbentry', data=db_name).exists():
		print("Not importing blast %s because database %s doesn't exist" % (blast_name, db_name))
		sys.exit(1)
	try:
		create_blast(db_name, sample_name, filename)
		ImportedData.objects.create(type='blast', data=blast_name)
	except Exception as e:
		inserter.rollback()
		extra_inserter.rollback()
		raise
