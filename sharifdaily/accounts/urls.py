from django.conf.urls import patterns, include, url
from tastypie.api import Api
from .api import CreateUserResource, UserResource, UserProfileResource

api = Api(api_name='v1')
api.register(CreateUserResource())
api.register(UserResource())
api.register(UserProfileResource())

urlpatterns = patterns('',
	(r'^api/', include(api.urls)),
)
