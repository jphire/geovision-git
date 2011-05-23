from django.db import models
from django.contrib.auth.models import User


class Collection(models.Model):
	name = models.CharField(max_length=32)
	description = models.TextField()
	users = models.ManyToManyField(User)

class Sample(models.Model):
	sample_id = models.CharField(max_length=32)
	collection = models.ForeignKey(Collection)