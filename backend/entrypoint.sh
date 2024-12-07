#!/bin/sh
# Wait for Postgres to be ready
/wait-for-postgres.sh db

sleep 5

# Perform database migration
poetry run python manage.py makemigrations
poetry run python manage.py migrate

# Create superuser
poetry run python create_superuser.py

# Collect static files
python manage.py collectstatic --noinput

# Start Django application with Gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120 --max-requests 1000 --max-requests-jitter 50
