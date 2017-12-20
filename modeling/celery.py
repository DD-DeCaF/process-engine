
"""
=============
Celery Config
=============
Celery preferences and general tasks.
"""
from __future__ import absolute_import
import logging
import os

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modeling.settings')

app = Celery('modeling')  # pylint: disable=invalid-name
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
