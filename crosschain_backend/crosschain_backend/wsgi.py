"""
WSGI config for crosschain_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

from os import environ

from django.core.wsgi import get_wsgi_application

environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'crosschain_backend.settings.base',
)

application = get_wsgi_application()
