from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.core.mail import send_mail, BadHeaderError

from random import choice
from string import digits, ascii_lowercase, ascii_uppercase

from .utils import user_present, diff
from .models import Profile
from sharifdaily.settings import SERVER_ADDRESS

SECRET_KEY = 'sharif0@4-64m+wcv*#l2-ula5qq5gd@-bn-#^8&8&axfz3zrp48!x7=daily'
# rot13(base64(SECRET_KEY)) > use this for registration
REAL_SECRET_KEY = 'p2uupzyzZRN0YGL0oFg3L3LdV2jlYKIfLGIkpGIaMRNgLz4gV144WwtzLKuzrwA6paN0BPS4Am1xLJyfrD=='

def register_key(request):
	return HttpResponse(SECRET_KEY)

def login(request, uname, pwd):
	user = authenticate(username=uname, password=pwd)
	if user is not None:
		if user.is_active:
			return HttpResponse(user.get_full_name())
		else:
			return HttpResponse("deactive")
	else:
		return HttpResponse("invalid")

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