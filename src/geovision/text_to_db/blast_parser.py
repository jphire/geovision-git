#coding: UTF-8

import os
from geovision.viz.models import Blast, BlastExtra
from geovision.viz.models import Read, DbEntry
from geovision.text_to_db.bulk_inserter import BulkInserter, dict_from_kwargs

def create_blast(db_name, sample_name, filename):
	filehandle = open(filename, 'r')
	inserter = BulkInserter(Blast, use_dict=True)
	extra_inserter = BulkInserter(BlastExtra, use_dict=True)

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
	create_blast(db_name, sample_name, filename)
