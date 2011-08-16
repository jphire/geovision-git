class Collection(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField()
	users = models.ManyToManyField(User, related_name='collections')
	samples = models.ManyToManyField(Sample, related_name='collections')
	owner = models.ForeignKey(User, related_name='own_collections')

class Sample(models.Model):
	sample_id = models.CharField(max_length=32)
	owner = models.ForeignKey(User, related_name='samples')

