from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

class Archive(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=144)
	pdf = models.FileField(upload_to='archives/', max_length=200, blank=False)
	tag = models.CharField(max_length=144, blank=True) # for storing arbitrary data

	def __unicode__(self):
		return unicode(self.title)

class Article(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	headline = models.CharField(max_length=144)
	content = models.TextField()
	view_count = models.IntegerField(blank=True, null=True, default=0)
	published = models.BooleanField(default=False)
	tag = models.CharField(max_length=144, blank=True) # for storing arbitrary data

	photo = models.ImageField(upload_to='article_photos/', blank=True)
	photo_thumbnail = ImageSpecField(source='photo',
                                      processors=[ResizeToFill(200, 150)],
                                      format='JPEG',
                                      options={'quality': 70})
	def __unicode__(self):
		return unicode("%s: %s" % (self.headline[:30], self.content[:60]))


class Report(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	headline = models.CharField(max_length=144)
	author = models.ForeignKey(User, related_name="reports")
	content = models.TextField(blank=True)
	view_count = models.IntegerField(blank=True, null=True, default=0)
	published = models.BooleanField(default=False)
	tag = models.CharField(max_length=144, blank=True) # for storing arbitrary data

	photo = ProcessedImageField(upload_to='report_photos/',
								processors=[ResizeToFill(640, 480)],
								format='JPEG',
								options={'quality': 70},
								blank=True)
	audio = models.FileField(upload_to='report_audios/', max_length=200, blank=True)
	video = models.FileField(upload_to='report_videos/', max_length=200, blank=True)

	def __unicode__(self):
		return unicode("%s: %s" % (self.headline[:30], self.content[:60]))


class ArticleComment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, related_name="article_comments")
	content = models.TextField()
	article = models.ForeignKey(Article, related_name="comments")
	is_public = models.BooleanField(default=False)
	tag = models.CharField(max_length=144, blank=True) # for now I just use it to store an author's name

	def __unicode__(self):
		return unicode("%s: %s" % (self.article.headline, self.content[:60]))

class ReportComment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, related_name="report_comments")
	content = models.TextField()
	report = models.ForeignKey(Report, related_name="comments")
	is_public = models.BooleanField(default=False)
	tag = models.CharField(max_length=144, blank=True) # for now I just use it to store an author's name

	def __unicode__(self):
		return unicode("%s: %s" % (self.report.headline, self.content[:60]))

class Like(models.Model):
	user = models.ForeignKey(User, related_name="likes")
	article = models.ForeignKey(Article, related_name="likes", blank=True, null=True)
	report = models.ForeignKey(Report, related_name="likes", blank=True, null=True)