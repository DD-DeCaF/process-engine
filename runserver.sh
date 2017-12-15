#!/bin/sh
python manage.py migrate && gunicorn -w 2 -b 0.0.0.0:8000 modeling.wsgi:application