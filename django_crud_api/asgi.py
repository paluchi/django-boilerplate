"""
ASGI config for django_crud_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv()

application = get_asgi_application()
