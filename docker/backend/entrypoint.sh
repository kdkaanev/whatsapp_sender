#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

until python manage.py check --database default >/dev/null 2>&1
do
    sleep 2
done


echo "Starting Gunicorn..."

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -