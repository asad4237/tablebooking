#!/bin/bash

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput
#python manage.py runserver 0.0.0.0:8000

# Apply database migrations
echo "Apply database migrations"
python manage.py flush --noinput
python manage.py makemigrations restaurants
python manage.py migrate

echo "Creatign superuser with name asad (django-admin.py)"

#python manage.py createsuperuser --noinput
#python manage.py createsuperuser  --noinput

echo "Create users and groups"
python manage.py startup_command

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8877