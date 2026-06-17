"""
WSGI config for the Fill & Go project.

Exposes the WSGI callable as a module-level variable named ``application``.
This is what gunicorn / any WSGI server points to in production.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fillandgo.settings')

application = get_wsgi_application()
