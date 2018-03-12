# Copyright 2018 Novo Nordisk Foundation Center for Biosustainability, DTU.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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