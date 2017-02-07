"""
WSGI config for unsplash_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.template.backends import django
from whitenoise.django import DjangoWhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unsplash_backend.settings")

application = get_wsgi_application()
application = django.core.handlers.wsgi.WSGIHandler()
application = DjangoWhiteNoise(application)
