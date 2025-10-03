#!/usr/bin/env python
import os
import sys
import django
from django.db import connection

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protrack.settings')

# Setup Django
django.setup()

from api.models import DeviceData

def reset_ranking_sequence():
    """Reset the ranking_id sequence to start from 1"""
    print("🔄 Resetting ranking sequence...")
    
    # First, clear all existing data
    deleted_count = DeviceData.objects.count()
    DeviceData.objects.all().delete()
    print(f"🗑️  Deleted {deleted_count} existing records")
    
    # Reset the sequence to start from 1
    with connection.cursor() as cursor:
        # For PostgreSQL
        cursor.execute("ALTER SEQUENCE api_devicedata_ranking_id_seq RESTART WITH 1;")
        print("✅ Reset sequence to start from 1")
    
    print("✅ Database is ready for new data with ranking starting from 1")
    print("\nNext steps:")
    print("1. Run: python manage.py fetch_tracking_data")
    print("2. Run: python manage.py load_device_data response_logs/[latest_folder]/all_records.json")

if __name__ == "__main__":
    confirm = input("⚠️  This will DELETE ALL existing data and reset rankings to start from 1. Continue? (yes/no): ")
    if confirm.lower() == 'yes':
        reset_ranking_sequence()
    else:
        print("Operation cancelled.")