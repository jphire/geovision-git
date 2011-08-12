from django.db import models

class Pathway(models.Model):
	id = models.CharField(max_length=5, primary_key=True)
	name = models.CharField(max_length=128)

class Enzyme(models.Model):
	ec_number = models.CharField(max_length=13, primary_key=True)
	pathways = models.ManyToManyField(Pathway, related_name='enzymes')

class EnzymeName(models.Model):
	ec_number = models.CharField(max_length=13)
	enzyme_name = models.CharField(max_length=128)

