from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^accounts/', include('sharifdaily.accounts.urls')),
    url(r'^newspaper/', include('sharifdaily.newspaper.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if 'SERVE_STATIC' in dir(settings):
	if settings.SERVE_STATIC:
		urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
