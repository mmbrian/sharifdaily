from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.core.mail import send_mail, BadHeaderError
from django.core.serializers.json import DjangoJSONEncoder

from random import choice
from string import digits, ascii_lowercase, ascii_uppercase

from .utils import user_present, diff
from .models import Profile, UserHistory
from sharifdaily.settings import SERVER_ADDRESS

try:
    import json
except ImportError:
   from django.utils import simplejson as json

SECRET_KEY = 'sharif0@4-64m+wcv*#l2-ula5qq5gd@-bn-#^8&8&axfz3zrp48!x7=daily'
# rot13(base64(SECRET_KEY)) > use this for registration
REAL_SECRET_KEY = 'p2uupzyzZRN0YGL0oFg3L3LdV2jlYKIfLGIkpGIaMRNgLz4gV144WwtzLKuzrwA6paN0BPS4Am1xLJyfrD=='

HISTORYITEMS_PER_PAGE = 10


def register_key(request):
	return HttpResponse(SECRET_KEY)

def login(request, uname, pwd):
	user = authenticate(username=uname, password=pwd)
	if user is not None:
		if user.is_active:
			user_id        = user.id
			user_full_name = user.get_full_name()
			user_major     = ''
			user_avatar    = ''
			try:
				user_major = user.profile.major
				user_avatar= user.profile.avatar.url # sth like /uploads/avatars/...
			except ValueError:
				user_avatar= ''
			except Profile.DoesNotExist:
				user_major = ''
				user_avatar= ''

			keys = ["id", "full_name", "major", "avatar_url"]
			values = [user_id, user_full_name, user_major, user_avatar]
			return HttpResponse(json.dumps(dict(zip(keys, values)), cls=DjangoJSONEncoder))
		else:
			return HttpResponse("deactive")
	else:
		return HttpResponse("invalid")

def get_user_history(request, user_id, page):
	history_list = UserHistory.objects.filter(owner__id = int(user_id)).values('id', 'created', 'action', 'content').order_by('-created')
	page = int(page)
	start = (page - 1) * HISTORYITEMS_PER_PAGE
	end = page * HISTORYITEMS_PER_PAGE
	return HttpResponse(json.dumps(list(history_list[start:end]), cls=DjangoJSONEncoder))

@csrf_exempt
def post_user_history(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			user_id = request.POST['user_id']
			action  = request.POST['action']
			content = request.POST['content']
			try:
				user = User.objects.get(id=user_id)
				item = UserHistory(owner=user, action=action, content=content)
				item.save()
				return HttpResponse(str(item.id))
			except User.DoesNotExist:
				return HttpResponse('invalid user')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def change_password(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			uname = request.POST['username']
			pwd   = request.POST['old_password']
			user  = authenticate(username=uname, password=pwd)
			if user is not None:
				new_pwd = request.POST['new_password']
				user.set_password(new_pwd)
				user.save()
				return HttpResponse('changed')
			else:
				return HttpResponse('invalid user')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def change_picture(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			user_id = request.POST['user_id']
			try:
				user = User.objects.get(id=int(user_id))
				request_type = request.POST.get('type', '')
				image = request.FILES.get('image', None)
				if (request_type == 'set'):
					user.profile.avatar = image
					user.profile.save()
					return HttpResponse(user.profile.avatar.url)		
				else:
					user.profile.avatar.delete()
					user.profile.save()
					return HttpResponse("deleted")
			except User.DoesNotExist:
				return HttpResponse("invalid user")
			except Exception as error:
				# return HttpResponse(str(error))
				return HttpResponse('invalid operation')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def register(request):
	if request.method == 'POST':
		key = request.POST['key']
		# if (key == REAL_SECRET_KEY):
		if diff(key, REAL_SECRET_KEY) < 3:
			username = request.POST['username']
			email = request.POST['email']
			if not user_present(username, email):
				password = request.POST['password']
				user = User.objects.create_user(username, email, password)
				user.first_name = request.POST['first_name']
				user.last_name = request.POST['last_name']
				user.is_active = False
				user.save()

				confirmation_code = ''.join(choice(ascii_uppercase + digits + ascii_lowercase) for x in xrange(33))
				major = request.POST['major']
				profile, new = Profile.objects.get_or_create(user=user, confirmation_code=confirmation_code, major=major)
				profile.save()
				send_confirmation_email(username, email, confirmation_code)

				return HttpResponse("created")
			else:
				return HttpResponse("exists")
		else:
			return HttpResponse("invalid")

def activate(request, username, confirmation_code):
	try:
		user = User.objects.get(username=username)
		profile = user.profile
		valid_code = profile.confirmation_code == confirmation_code
		if valid_code:
			user.is_active = True
			user.save()
		return render_to_response('accounts/signup_complete.html', locals())
	except User.DoesNotExist:
		return HttpResponse('invalid')


def send_confirmation_email(username, to_email, confirmation_code):
	message = 'Greetings!\n\nVisit %saccounts/activate/%s/%s in order to activate your account.\n\nThanks' % (SERVER_ADDRESS, username, confirmation_code)
	send_mail('Your SharifDaily Account', message, 'SharifDaily Newspaper', [to_email])


# TODO Post Profile Picture, Get/Post History, Post New Password 