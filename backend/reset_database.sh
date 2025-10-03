#!/bin/bash

# Complete database reset script
# WARNING: This will delete ALL data and reset migrations

echo "WARNING: This will completely reset your database!"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

# Activate virtual environment
source venv/bin/activate

# Remove migration files (keep __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Drop and recreate database (PostgreSQL)
# Note: Adjust database name and credentials as needed
dropdb -U postgres protrack_db 2>/dev/null || true
createdb -U postgres protrack_db

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

echo "Database has been completely reset!"