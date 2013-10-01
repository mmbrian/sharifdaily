from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .utils import user_present

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
		if (key == REAL_SECRET_KEY):
			username = request.POST['username']
			email = request.POST['email']
			if not user_present(username, email):
				password = request.POST['password']
				user = User.objects.create_user(username, email, password)
				user.first_name = request.POST['first_name']
				user.last_name = request.POST['last_name']

			else:
				return HttpResponse("exists")			
		else:
			return HttpResponse("invalid")		

