from django.conf.urls import patterns, include, url


urlpatterns = patterns('sharifdaily.accounts.views',
	url(r'^login/(?P<uname>.*)/(?P<pwd>.*)', 'login'),

	url(r'^activate/(?P<username>.*)/(?P<confirmation_code>.*)', 'activate'),
	url(r'^register/get_registeration_key', 'register_key'),
	url(r'^register$', 'register'),
	url(r'^change_password$', 'change_password'),
	url(r'^change_picture$', 'change_picture'),
)
