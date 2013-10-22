from django.conf.urls import patterns, include, url

urlpatterns = patterns('sharifdaily.kernel.views',
	url(r'^version/latest$', 'get_latest_version'),
)