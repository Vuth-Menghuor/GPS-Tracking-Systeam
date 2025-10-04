#!/usr/bin/env bash
# Render build script for Django

set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Debug: Show environment info
echo "🔍 DATABASE_URL status:"
if [ -n "$DATABASE_URL" ]; then
    echo "✅ DATABASE_URL is set"
    echo "🔗 Database URL starts with: ${DATABASE_URL:0:20}..."
    echo "🔄 Running migrations..."
    python manage.py migrate
    echo "✅ Migrations completed"
else
    echo "❌ DATABASE_URL not set, skipping migrations"
    echo "📋 Available environment variables:"
    env | grep -E "(DATABASE|DB_)" || echo "No database environment variables found"
fi