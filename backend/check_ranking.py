#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protrack.settings')

# Setup Django
django.setup()

from api.models import DeviceData

# Check ranking IDs
total_records = DeviceData.objects.count()
print(f'Total records: {total_records}')

if total_records > 0:
    first_10 = DeviceData.objects.all().order_by('ranking_id')[:10]
    print('\nFirst 10 ranking IDs:')
    for d in first_10:
        print(f'#{d.ranking_id}: {d.imei}')
    
    # Check if we have consecutive IDs starting from 1
    first_id = DeviceData.objects.all().order_by('ranking_id').first().ranking_id
    print(f'\nFirst ranking ID: {first_id}')
    
    # Check last ID
    last_id = DeviceData.objects.all().order_by('ranking_id').last().ranking_id
    print(f'Last ranking ID: {last_id}')
    
    if first_id != 1:
        print(f'\n⚠️  Ranking does not start from 1! It starts from {first_id}')
        print('This explains why the UI doesn\'t show rankings starting from 1.')
    else:
        print('\n✅ Ranking starts from 1 as expected.')
else:
    print('No records found in database.')