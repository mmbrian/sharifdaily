from django.db import models

class AppVersion(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	version_code = models.IntegerField(default=1)
	version_name = models.CharField(max_length=144, blank=True)
	published = models.BooleanField(default=False)
	apk = models.FileField(
		upload_to=lambda i, fn: 'apks/%s_%s%s' \
		% (fn[:fn.rindex('.')] if '.' in fn else fn,
		   i.version_code, 
		   fn[fn.rindex('.'):] if '.' in fn else '.apk'), 
		max_length=200, blank=False)

	def __unicode__(self):
		return unicode(self.version_code)
