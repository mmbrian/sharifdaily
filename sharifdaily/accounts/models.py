from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

class UserHistory(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	action = models.CharField(max_length=60)
	content = models.TextField()
	owner = models.ForeignKey(User, related_name="history")

class UserProfile(models.Model):
	'''
	A model to store extra info for each user
	'''
	user = models.OneToOneField(User, related_name='profile')
	avatar = models.ImageField(upload_to='/avatars/')
	major = models.CharField(max_length=144)

	def __unicode__(self):
		return self.user.get_full_name()

# Signals
def signals_import():
	from tastypie.models import create_api_key
	models.signals.post_save.connect(create_api_key, sender=User)
signals_import()
