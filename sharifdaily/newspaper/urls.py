from django.conf.urls import patterns, include, url

urlpatterns = patterns('sharifdaily.newspaper.views',
	# url(r'^login/(?P<uname>.*)/(?P<pwd>.*)', 'login')
	url(r'^ads/$', 'get_ads'),

	url(r'^articles/latest/(?P<page>[0-9]+)/$', 'get_last_article_id'),
	url(r'^articles/page/(?P<page>[0-9]+)/$', 'get_articles'),
	url(r'^articles/mostviewed/page/(?P<page>[0-9]+)/$', 'get_most_viewed_articles'),
	url(r'^articles/mostliked/page/(?P<page>[0-9]+)/$', 'get_most_liked_articles'),
	url(r'^archives/page/(?P<page>[0-9]+)/$', 'get_main_archives'),
	url(r'^archives/other/page/(?P<page>[0-9]+)/$', 'get_other_archives'),
	url(r'^reports/latest/(?P<page>[0-9]+)/$', 'get_last_report_id'),
	url(r'^reports/page/(?P<page>[0-9]+)/$', 'get_reports'),
	url(r'^reports/mostviewed/page/(?P<page>[0-9]+)/$', 'get_most_viewed_reports'),
	url(r'^reports/mostliked/page/(?P<page>[0-9]+)/$', 'get_most_liked_reports'),
	url(r'^podcasts/page/(?P<page>[0-9]+)/$', 'get_podcasts'),

	url(r'^articles/comments/page/(?P<page>[0-9]+)/(?P<_id>[0-9]+)/$', 'get_article_comments'),
	url(r'^reports/comments/page/(?P<page>[0-9]+)/(?P<_id>[0-9]+)/$', 'get_report_comments'),
	url(r'^articles/likes/(?P<_id>[0-9]+)/$', 'get_article_likes'),
	url(r'^reports/likes/(?P<_id>[0-9]+)/$', 'get_report_likes'),
	url(r'^articles/likes/(?P<user_id>[0-9]+)/(?P<article_id>[0-9]+)/$', 'has_liked_article'),
	url(r'^reports/likes/(?P<user_id>[0-9]+)/(?P<report_id>[0-9]+)/$', 'has_liked_report'),

	url(r'^articles/thumbnails/(?P<_id>[0-9]+)/$', 'get_article_photo_thumbnail'),
	url(r'^articles/likes_thumbnails/(?P<_id>[0-9]+)/$', 'get_article_likes_and_thumbnail'),

	# POSTs
	url(r'^articles/comments/post$', 'post_article_comment'),
	url(r'^reports/comments/post$', 'post_report_comment'),
	
	url(r'^articles/article/like$', 'post_article_like'),
	url(r'^articles/article/unlike$', 'post_article_unlike'),
	url(r'^reports/report/like$', 'post_report_like'),
	url(r'^reports/report/unlike$', 'post_report_unlike'),
	
	url(r'^articles/article/view$', 'view_article'),
	url(r'^reports/report/view$', 'view_report'),

	url(r'^reports/report/post$', 'post_report'),
)