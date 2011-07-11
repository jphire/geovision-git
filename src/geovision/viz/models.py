from django.db import models
from geovision.userdb.models import Sample

class Read(models.Model):
	sample = models.CharField(max_length=32)
	read_id = models.CharField(max_length=64, primary_key=True)
	description = models.TextField()
	data = models.TextField()

	@classmethod
	def deferred(cls):
#		return cls.objects
		return Read.objects.all().defer('data')

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

	@classmethod
	def deferred(cls):
#		return cls.objects
		return DbEntry.objects.all().defer('data')

class DbUniprotEcs(models.Model):
	db_id = models.ForeignKey(DbEntry, db_column='db_id', related_name='uniprot_ecs')
	protein_existence_type = models.CharField(max_length=4)
	ec = models.CharField(max_length=12)

class Blast(models.Model):
	read = models.ForeignKey(Read)
	database_name = models.CharField(max_length=16)
	db_entry = models.ForeignKey(DbEntry)
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
	read_seq = models.TextField()
	db_seq = models.TextField()

	@classmethod
	def deferred(cls):
		return Blast.objects.all().only('read', 'database_name', 'db_entry', 'error_value', 'bitscore', 'length')

class Result(models.Model): # Query_seq_id Target_seq_id Evident_type E.C._number p_value Bit_score
	read = models.CharField(max_length=64)
	db_entry = models.CharField(max_length=32)
	evident_type = models.CharField(max_length = 2)
	ec_number = models.CharField(max_length = 32)
	error_value = models.FloatField()
	bitscore = models.FloatField()

class EnzymeName(models.Model):
	ec_number = models.CharField(max_length=12)
	enzyme_name = models.CharField(max_length=128)

class Pathway(models.Model):
	id = models.CharField(max_length=6, primary_key=True)
	name = models.CharField(max_length=64)

class Compound(models.Model):
	id = models.CharField(max_length=6, primary_key=True)
	pathways = models.ManyToManyField(Pathway, related_name='compounds')

class Enzyme(models.Model):
	ec_number = models.CharField(max_length=12, primary_key=True)
	pathways = models.ManyToManyField(Pathway, related_name='enzymes')

class Reaction(models.Model):
	id = models.CharField(max_length=6, primary_key=True)
	name = models.CharField(max_length=32)
	equation = models.CharField(max_length=64)
	enzyme = models.ForeignKey(Enzyme, related_name='reactions')
	compounds = models.ManyToManyField(Pathway, related_name='reactions')
