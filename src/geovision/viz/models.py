from django.db import models
from meta.models import *

class Read(models.Model):
	sample = models.CharField(max_length=16)
	read_id = models.CharField(max_length=64, primary_key=True)
	description = models.TextField()
	data = models.TextField()

	deferred_fields = ('data',)
	@classmethod
	def deferred(cls):
		return cls.objects.all().defer(*cls.deferred_fields)

class DbEntry(models.Model):
	source_file = models.CharField(max_length=16)
	db_id = models.CharField(max_length=32, primary_key=True)
	description = models.TextField()
	data = models.TextField()
	# Uniprot-specific fields below
	sub_db = models.CharField(max_length=4, blank=True)
	entry_name = models.CharField(max_length=16, blank=True)
	os_field = models.CharField(max_length=128, blank=True)
	other_info = models.TextField(blank=True)

	deferred_fields = ('data',)
	@classmethod
	def deferred(cls):
		return cls.objects.all().defer(*cls.deferred_fields)

class DbUniprotEcs(models.Model):
	db_id = models.ForeignKey(DbEntry, db_column='db_id', related_name='uniprot_ecs')
	protein_existence_type = models.CharField(max_length=4)
	ec = models.CharField(max_length=13)

class Blast(models.Model):
	read = models.ForeignKey(Read)
	sample = models.CharField(max_length=16)
	database_name = models.CharField(max_length=16)
	db_entry = models.ForeignKey(DbEntry)
	error_value = models.FloatField()
	bitscore = models.FloatField()

	deferred_fields = ()
	@classmethod
	def deferred(cls):
		return cls.objects.all().defer(*cls.deferred_fields)

class BlastExtra(models.Model):
	blast = models.ForeignKey(Blast, primary_key=True)
	pident = models.FloatField()
	length = models.IntegerField()
	mismatch = models.IntegerField()
	gapopen = models.IntegerField()
	qstart = models.IntegerField()
	qend = models.IntegerField()
	sstart = models.IntegerField()
	send = models.IntegerField()
	read_seq = models.TextField()
	db_seq = models.TextField()

class BlastEcs(models.Model):
	ec = models.CharField(max_length=13)
	sample = models.CharField(max_length=16)
	db_entry = models.ForeignKey(DbEntry)
	bitscore = models.FloatField()
	error_value = models.FloatField()
