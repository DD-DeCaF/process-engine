#!/bin/sh
python manage.py migrate && \
python manage.py createsuperuser_password --username $SUPERUSER_USERNAME --email $SUPERUSER_USERNAME --password $SUPERUSER_PASSWORD --preserve && \
python manage.py register && \
gunicorn -w 1 -b 0.0.0.0:8000 -t 150 modeling.wsgi:application