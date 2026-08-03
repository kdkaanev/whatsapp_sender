#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

until python manage.py check --database default >/dev/null 2>&1
do
    sleep 2
done

echo "PostgreSQL is ready."

exec celery -A config worker --loglevel=info