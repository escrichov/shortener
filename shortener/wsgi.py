"""
WSGI config for shortener project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
import os
import sys

configuration = os.getenv('ENVIRONMENT', 'development').title()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shortener.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, "apps"))

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
