#!/usr/bin/env bash
# Render build script for Django

set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Only run migrations if DATABASE_URL is set (production)
if [ -n "$DATABASE_URL" ]; then
    python manage.py migrate
else
    echo "DATABASE_URL not set, skipping migrations"
fi