"""Celery configuration."""
from __future__ import absolute_import, division, print_function, unicode_literals

import os

try:
    from celery import Celery
except ImportError:
    Celery = None

from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modeling.settings")


app = None  # pylint: disable=invalid-name
if Celery:
    app = Celery('modeling')  # pylint: disable=invalid-name

    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)