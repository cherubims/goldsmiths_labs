#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn goldsmiths_labs.wsgi:application

gunicorn goldsmiths_labs.wsgi:application --bind 0.0.0.0:8000 &   # Run Gunicorn in the background
daphne -b 0.0.0.0 -p 8001 goldsmiths_labs.asgi:application         # Run Daphne on a separate port