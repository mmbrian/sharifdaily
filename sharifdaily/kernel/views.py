from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from .models import AppVersion

try:
    import json
except ImportError:
   from django.utils import simplejson as json


def get_latest_version(request):
    try:
        last_version = AppVersion.objects.filter(published=True).values('version_code', 'version_name', 'apk').order_by('-date')[0]
        return HttpResponse(json.dumps(last_version, cls=DjangoJSONEncoder))
    except:
        return HttpResponse('-1')    
