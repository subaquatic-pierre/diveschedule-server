#!/bin/bash
python3 manage.py makemigrations
until python3 manage.py migrate; do
  sleep 2
  echo "Retry!";
done

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py createsuperuser --noinput
python3 manage.py loaddata admin
# python3 manage.py loaddata users profiles days bookings
echo "Django is ready.";

path="$(pwd)/app/wsgi/uwsgi.ini"

uwsgi --ini "$path"