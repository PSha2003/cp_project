"""
ASGI config for cp_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cp_project.settings")

#application = get_asgi_application()
application = ASGIStaticFilesHandler(get_asgi_application())
