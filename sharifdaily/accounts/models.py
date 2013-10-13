from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class UserHistory(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	action = models.CharField(max_length=60)
	content = models.TextField(blank=True)
	owner = models.ForeignKey(User, related_name="history")

	def __unicode__(self):
		return unicode("%s -> %s: %s" % (self.owner.get_full_name(), self.action, self.content))

class Profile(models.Model):
	'''
	A model to store extra info for each user
	'''
	user = models.OneToOneField(User, related_name='profile')
	confirmation_code = models.CharField(max_length=144, blank=True)

	avatar = ProcessedImageField(upload_to='avatars/',
								processors=[ResizeToFill(128, 128)],
								format='JPEG',
								options={'quality': 70},
								blank=True)
	major = models.CharField(max_length=144, blank=True)

	def __unicode__(self):
		return unicode(self.user.get_full_name())

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     """Create a matching profile whenever a user object is created."""
#     if created: 
#         profile, new = Profile.objects.get_or_create(user=instance)