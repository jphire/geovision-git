from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save

class Sample(models.Model):
	sample_id = models.CharField(max_length=32)
#	owner = models.ForeignKey(User, related_name='samples')
#
#class Collection(models.Model):
#	name = models.CharField(max_length=64)
#	description = models.TextField()
#	users = models.ManyToManyField(User, related_name='collections')
#	samples = models.ManyToManyField(Sample, related_name='collections')
#	owner = models.ForeignKey(User, related_name='own_collections')
#
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	settings = models.TextField(blank=True)

def save_user_profile_pre_hook(sender, instance, **kwargs):
		instance.is_superuser = instance.is_staff
def save_user_profile_post_hook(sender, instance, created, **kwargs):
		obj, is_new = UserProfile.objects.get_or_create(user=instance)
		if is_new:
			obj.settings = {}
	
pre_save.connect(save_user_profile_pre_hook, sender=User)
post_save.connect(save_user_profile_post_hook, sender=User)

