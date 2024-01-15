"""
WSGI config for django_crud_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()
application = get_wsgi_application()
