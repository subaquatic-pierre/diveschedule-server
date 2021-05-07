#!/bin/bash
python manage.py makemigrations
until python manage.py migrate; do
  sleep 2
  echo "Retry!";
done
python manage.py shell < init_admin.py

python manage.py makemigrations
python manage.py migrate
python3 manage.py loaddata users profiles days bookings
echo "Django is ready.";

python manage.py runserver 0.0.0.0:8000