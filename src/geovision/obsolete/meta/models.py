class Compound(models.Model):
	id = models.CharField(max_length=5, primary_key=True)
	name = models.CharField(max_length=100)
	pathways = models.ManyToManyField(Pathway, related_name='compounds')

class Reaction(models.Model):
	id = models.CharField(max_length=6, primary_key=True)
	name = models.CharField(max_length=128)
#	equation = models.CharField(max_length=128)
	reactants = models.ManyToManyField(Compound, related_name='reactant_reactions')
	products = models.ManyToManyField(Compound, related_name='product_reactions')
	pathways = models.ManyToManyField(Pathway, related_name='reactions')
	enzymes = models.ManyToManyField(Enzyme, related_name='reactions')
