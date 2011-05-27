from django.db import models
from userdb.models import Sample

class Read(models.Model):
	sample = models.CharField(max_length=32)
	read_id = models.CharField(max_length=64)
	description = models.CharField(max_length=128)
	data = models.TextField()

class DbEntry(models.Model):
	source_file = models.CharField(max_length=32)
	read_id = models.CharField(max_length=64)
	description = models.CharField(max_length=128)
	data = models.TextField()


class Blast(models.Model): # qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore
	read = models.ForeignKey(Read)
	database_name = models.CharField(max_length=16)
	db_entry = models.ForeignKey(DbEntry)
	pident = models.DecimalField(max_digits=4,decimal_places=2)
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
	read = models.ForeignKey(Read)
	db_entry = models.ForeignKey(DbEntry)
	evident_type = models.CharField(max_length = 2)
	ec_number = models.CharField(max_length = 32)
	error_value = models.FloatField()
	bitscore = models.FloatField()
