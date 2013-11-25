from django.conf.urls import patterns, include, url


urlpatterns = patterns('sharifdaily.accounts.views',
	url(r'^login/(?P<uname>.*)/(?P<pwd>.*)', 'login'),

	url(r'^passwordreset/confirm/(?P<username>.*)/(?P<confirmation_code>.*)', 'confirm_pwd_reset'),
	url(r'^activate/(?P<username>.*)/(?P<confirmation_code>.*)', 'activate'),
	url(r'^register/get_registeration_key', 'register_key'),
	url(r'^register$', 'register'),
	url(r'^change_password$', 'change_password'),
	url(r'^reset_password$', 'reset_password'),
	url(r'^change_picture$', 'change_picture'),
	url(r'^history/post$', 'post_user_history'),
	url(r'^history/(?P<user_id>[0-9]+)/(?P<page>[0-9]+)/$', 'get_user_history'),
	url(r'^profile/(?P<user_id>[0-9]+)/$', 'get_user_profile'),
)
