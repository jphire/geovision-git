from django.db import models
from geovision.userdb.models import Sample

class Read(models.Model):
	sample = models.CharField(max_length=32)
	read_id = models.CharField(max_length=64)
	description = models.TextField()
	data = models.TextField()
	class Meta:
		unique_together = ("sample", "read_id")

class DbEntry(models.Model):
	source_file = models.CharField(max_length=32)
	db_id = models.CharField(max_length=32, primary_key=True)
	description = models.TextField()
	data = models.TextField()
	# Uniprot-specific fields below
	sub_db = models.CharField(max_length=4, blank=True)
	entry_name = models.CharField(max_length=16, blank=True)
	os_field = models.CharField(max_length=128, blank=True)
	other_info = models.TextField(blank=True)

class DbUniprotEcs(models.Model):
	db_id = models.CharField(max_length=32)
	protein_existence_type = models.CharField(max_length=4)
	ecs = models.CharField(max_length=128)

class Blast(models.Model): # qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore
	read = models.CharField(max_length=64)
	database_name = models.CharField(max_length=16)
	db_entry = models.CharField(max_length=32)
	pident = models.FloatField()
	length = models.IntegerField()
	mismatch = models.IntegerField()
	gapopen = models.IntegerField()
	qstart = models.IntegerField()
	qend = models.IntegerField()
	sstart = models.IntegerField()
	send = models.IntegerField()
	error_value = models.FloatField()
	bitscore = models.FloatField()

class Result(models.Model): # Query_seq_id    Target_seq_id   Evident_type    E.C._number     p_value Bit_score
	read = models.CharField(max_length=64)
	db_entry = models.CharField(max_length=32)
	evident_type = models.CharField(max_length = 2)
	ec_number = models.CharField(max_length = 32)
	error_value = models.FloatField()
	bitscore = models.FloatField()
