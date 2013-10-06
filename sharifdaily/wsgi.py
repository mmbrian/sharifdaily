"""
WSGI config for sharifdaily project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.
"""
import os, sys
import site

paths = ['/var/www/temp/sd/sharifdaily', 
		'/var/www/venvs/sharifdaily3-venv/bin', 
		'/var/www/venvs/sharifdaily3-venv/lib/python2.7/site-packages']
for path in paths:
	if path not in sys.path:
		sys.path.insert(0, path)

# activate virtualenv
activate_this = os.papaths = ['/var/www/temp/sd/sharifdaily', '/var/www/venvs/sharifdaily3-venv/bin']
for path in paths:
	if path not in sys.path:
		sys.path.append(path)
		th.expanduser('/var/www/venvs/sharifdaily3-venv/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
site.addsitedir('/var/www/venvs/sharifdaily3-venv/lib/python2.7/site-packages')

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "sharifdaily.settings"

# removing paths from outside virtual directory
# sys.path = filter(lambda path: not path.startswith('/usr'), sys.path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sharifdaily.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
