from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from imagekit.models import ProcessedImageField

class UserHistory(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	action = models.CharField(max_length=60)
	content = models.TextField()
	owner = models.ForeignKey(User, related_name="history")

class Profile(models.Model):
	'''
	A model to store extra info for each user
	'''
	user = models.OneToOneField(User, related_name='profile')
	avatar = ProcessedImageField(upload_to='/avatars/',
								processors=[ResizeToFill(100, 50)],
								format='JPEG',
								options={'quality': 60})
	major = models.CharField(max_length=144)

	def __unicode__(self):
		return self.user.get_full_name()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created: 
        profile, new = Profile.objects.get_or_create(user=instance)