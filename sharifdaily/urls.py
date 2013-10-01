from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sharifdaily.views.home', name='home'),
    # url(r'^sharifdaily/', include('sharifdaily.foo.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^accounts/', include('sharifdaily.accounts.urls')),
    url(r'^articles/', include('sharifdaily.newspaper.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
