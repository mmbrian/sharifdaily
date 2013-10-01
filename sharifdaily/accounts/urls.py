from django.conf.urls import patterns, include, url


urlpatterns = patterns('sharifdaily.accounts.views',
	url(r'^login/(?P<uname>.*)/(?P<pwd>.*)', 'login')
)
