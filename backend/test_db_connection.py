#!/usr/bin/env python3
"""
Simple script to test database connection on Render
"""
import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protrack.settings')

try:
    django.setup()
    
    from django.db import connection
    from django.core.management import execute_from_command_line
    
    # Test database connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        print(f"✅ Database connection successful! Result: {result}")
        
    # Check if tables exist
    from django.db import connection
    table_names = connection.introspection.table_names()
    print(f"📋 Available tables: {table_names}")
    
    # Try to run migrations if needed
    if not table_names or 'api_devicedata' not in table_names:
        print("🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed!")
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("🔍 Debug info:")
    print(f"DATABASE_URL set: {'DATABASE_URL' in os.environ}")
    if 'DATABASE_URL' in os.environ:
        db_url = os.environ['DATABASE_URL']
        # Don't print full URL for security, just show if it exists
        print(f"DATABASE_URL starts with: {db_url[:20]}...")
    else:
        print("DATABASE_URL not found in environment variables")