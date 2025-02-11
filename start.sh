#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn goldsmiths_labs.wsgi:application
