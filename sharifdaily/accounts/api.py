from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from tastypie.authentication import (
    Authentication, ApiKeyAuthentication, BasicAuthentication,
    MultiAuthentication)
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie import fields

from .models import UserProfile
from .utils import MINIMUM_PASS_LENGTH, validate_password
from .exceptions import CustomBadRequest


class CreateUserResource(ModelResource):
    user = fields.ForeignKey('core.api.UserResource', 'user', full=True)

    class Meta:
        allowed_methods = ['post']
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        queryset = UserProfile.objects.all()
        resource_name = 'create_user'
        always_return_data = True

    def hydrate(self, bundle):
        REQUIRED_USER_PROFILE_FIELDS = ("major", "user")
        for field in REQUIRED_USER_PROFILE_FIELDS:
            if field not in bundle.data:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))

        REQUIRED_USER_FIELDS = ("username", "email", "first_name", "last_name",
                                "raw_password")
        for field in REQUIRED_USER_FIELDS:
            if field not in bundle.data["user"]:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))
        return bundle

    def obj_create(self, bundle, **kwargs):
        try:
            email = bundle.data["user"]["email"]
            username = bundle.data["user"]["username"]
            if User.objects.filter(email=email):
                raise CustomBadRequest(
                    code="duplicate_exception",
                    message="That email is already used.")
            if User.objects.filter(username=username):
                raise CustomBadRequest(
                    code="duplicate_exception",
                    message="That username is already used.")
        except KeyError as missing_key:
            raise CustomBadRequest(
                code="missing_key",
                message="Must provide {missing_key} when creating a user."
                        .format(missing_key=missing_key))
        except User.DoesNotExist:
            pass

        # setting resource_name to `user_profile` here because we want
        # resource_uri in response to be same as UserProfileResource resource
        self._meta.resource_name = UserProfileResource._meta.resource_name
        return super(CreateUserResource, self).obj_create(bundle, **kwargs)


class UserResource(ModelResource):
    # We need to store raw password in a virtual field because hydrate method
    # is called multiple times depending on if it's a POST/PUT/PATCH request
    raw_password = fields.CharField(attribute=None, readonly=True, null=True,
                                    blank=True)

    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            BasicAuthentication(),
            ApiKeyAuthentication())
        authorization = Authorization()

        # Because this can be updated nested under the UserProfile, it needed
        # 'put'. No idea why, since patch is supposed to be able to handle
        # partial updates.
        allowed_methods = ['get', 'patch', 'put', ]
        always_return_data = True
        queryset = User.objects.all().select_related("api_key")
        excludes = ['is_active', 'is_staff', 'is_superuser', 'date_joined',
                    'last_login']

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id).select_related()

    def hydrate(self, bundle):
        if "raw_password" in bundle.data:
            # Pop out raw_password and validate it
            # This will prevent re-validation because hydrate is called
            # multiple times
            # https://github.com/toastdriven/django-tastypie/issues/603
            # "Cannot resolve keyword 'raw_password' into field." won't occur

            raw_password = bundle.data.pop["raw_password"]

            # Validate password
            if not validate_password(raw_password):
                if len(raw_password) < MINIMUM_PASSWORD_LENGTH:
                    raise CustomBadRequest(
                        code="invalid_password",
                        message=(
                            "Your password should contain at least {length} "
                            "characters.".format(length=
                                                 MINIMUM_PASSWORD_LENGTH)))
                raise CustomBadRequest(
                    code="invalid_password",
                    message=("Your password should contain at least one number"
                             ", one uppercase letter, one special character,"
                             " and no spaces."))

            bundle.data["password"] = make_password(raw_password)

        return bundle

    def dehydrate(self, bundle):
        bundle.data['key'] = bundle.obj.api_key.key

        try:
            # Don't return `raw_password` in response.
            del bundle.data["raw_password"]
        except KeyError:
            pass

        return bundle


class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            BasicAuthentication(),
            ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get', 'patch', ]
        detail_allowed_methods = ['get', 'patch', 'put']
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user).select_related()

    ## Since there is only one user profile object, call get_detail instead
    def get_list(self, request, **kwargs):
        kwargs["pk"] = request.user.profile.pk
        return super(UserProfileResource, self).get_detail(request, **kwargs)