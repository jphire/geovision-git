from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	settings = models.TextField(blank=True)

class SavedView(models.Model):
	user_profile = models.ForeignKey(UserProfile, related_name='saved_views')
	name = models.CharField(max_length=32)
	graph = models.TextField()
	query = models.TextField()

def save_user_profile_pre_hook(sender, instance, **kwargs):
		"""Make sure that staff status equals superuser status to simplify the admin ui."""
		instance.is_superuser = instance.is_staff

def save_user_profile_post_hook(sender, instance, created, **kwargs):
		"""Make sure that UserProfiles are created for each user"""
		obj, is_new = UserProfile.objects.get_or_create(user=instance)
		if is_new:
			obj.settings = {}
	
pre_save.connect(save_user_profile_pre_hook, sender=User)
post_save.connect(save_user_profile_post_hook, sender=User)

