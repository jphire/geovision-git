from django.db import models

class Pathway(models.Model):
	id = models.CharField(max_length=8, primary_key=True)
	name = models.CharField(max_length=128)

class Compound(models.Model):
	id = models.CharField(max_length=5, primary_key=True)
	name = models.CharField(max_length=100)
	pathways = models.ManyToManyField(Pathway, related_name='compounds')

class Enzyme(models.Model):
	ec_number = models.CharField(max_length=13, primary_key=True)
	pathways = models.ManyToManyField(Pathway, related_name='enzymes')

class Reaction(models.Model):
	id = models.CharField(max_length=6, primary_key=True)
	name = models.CharField(max_length=128)
#	equation = models.CharField(max_length=128)
	reactants = models.ManyToManyField(Compound, related_name='reactants')
	products = models.ManyToManyField(Compound, related_name='reactions')
	pathways = models.ManyToManyField(Pathway, related_name='reactions')
	enzymes = models.ManyToManyField(Enzyme, related_name='reactions')

class EnzymeName(models.Model):
	ec_number = models.CharField(max_length=13)
	enzyme_name = models.CharField(max_length=128)

