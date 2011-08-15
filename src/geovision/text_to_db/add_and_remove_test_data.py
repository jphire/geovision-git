#! /usr/bin/python
from geovision.text_to_db.graph_JSON import *

def create_blast(**kwargs):
	kwargs['read'] = Read.objects.get(pk=kwargs['read'])
	kwargs['db_entry'] = DbEntry.objects.get(pk=kwargs['db_entry'])
	normal_fields = ('read', 'db_entry', 'database_name', 'sample', 'error_value', 'bitscore')
	Blast.objects.create(**dict([(k, v) for (k, v) in kwargs.iteritems() if k in normal_fields]))


def create_test_data():
	Read.objects.create(sample="TEST", read_id="R1", description="bazz", data='ASD')
	Read.objects.create(sample="TEST", read_id="R2", description="baz", data='ASD')
	Read.objects.create(sample="TEST", read_id="R3", description="baz", data='ASD')
	Read.objects.create(sample="TEST", read_id="R4", description="baz", data='ASD')
	Read.objects.create(sample="TEST", read_id="R5", description="baz", data='ASD')
	Read.objects.create(sample="TEST", read_id="R6", description="baz", data='ASD')

	DbEntry.objects.create(source_file = "uniprot", db_id = "DB1", description="test", data='ASD', sub_db="sub", entry_name = "entryname", os_field="osfield", other_info = "otherinfo")
	DbEntry.objects.create(source_file = "frnadb", db_id = "DB2", description="test", data='ASD')
	DbEntry.objects.create(source_file = "frnadb", db_id = "DB3", description="test", data='ASD')
	DbEntry.objects.create(source_file = "frnadb", db_id = "DB4", description="test", data='ASD')
	DbEntry.objects.create(source_file = "frnadb", db_id = "DB5", description="test", data='ASD')
	DbEntry.objects.create(source_file = "frnadb", db_id = "DB6", description="test", data='ASD')
	DbEntry.objects.create(source_file = "frnadb", db_id = "DB7", description="test", data='ASD')

	create_blast(read="R1", database_name = "uniprot", db_entry="DB1", error_value=0.005, bitscore=200, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
	create_blast(read="R1", database_name = "uniprot", db_entry="DB2", error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
	create_blast(read="R1", database_name = "uniprot", db_entry="DB3", error_value=0.005, bitscore=600, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
	create_blast(read="R1", database_name = "uniprot", db_entry="DB4", error_value=0.005, bitscore=800, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
	create_blast(read="R2", database_name = "uniprot", db_entry="DB1", error_value=0.005, bitscore=1000, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
	create_blast(read="R3", database_name = "uniprot", db_entry="DB1", error_value=0.005, bitscore=300, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
	create_blast(read="R4", database_name = "uniprot", db_entry="DB2", error_value=0.005, bitscore=400, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
	create_blast(read="R5", database_name = "uniprot", db_entry="DB3", error_value=0.005, bitscore=700, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
	create_blast(read="R1", database_name = "uniprot", db_entry="DB4", error_value=0.005, bitscore=1100, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)
	create_blast(read="R1", database_name = "uniprot", db_entry="DB5", error_value = 0.005, bitscore=1500, pident=3, length = 20, mismatch=2, gapopen = 2, qstart= 2, qend = 2, sstart= 3,send=2)


def remove_test_data():
	read_list = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
	db_list = ['DB1', 'DB2', 'DB3', 'DB4', 'DB5', 'DB6', 'DB7']
	Read.objects.filter(read_id__in=read_list).delete()
	DbEntry.objects.filter(db_id__in=db_list).delete()
	Blast.objects.filter(read__read_id__in=read_list).delete()

if __name__ == "__main__":
    print "Hello World";
