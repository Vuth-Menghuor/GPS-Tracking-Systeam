import json
import os
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import DeviceData


class Command(BaseCommand):
    help = 'Load device data from JSON file into database'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Path to JSON file containing device data'
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear all existing data before loading new data',
        )

    def handle(self, *args, **options):
        json_file = options['json_file']
        clear_existing = options['clear_existing']

        # Check if file exists
        if not os.path.exists(json_file):
            raise CommandError(f'JSON file not found: {json_file}')

        try:
            # Load JSON data
            self.stdout.write(f'📂 Loading data from: {json_file}')
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.stdout.write(self.style.SUCCESS(f'✅ Loaded {len(data)} records from JSON'))

            # Clear existing data if requested
            if clear_existing:
                self.stdout.write('🗑️ Clearing existing device data...')
                deleted_count = DeviceData.objects.all().delete()[0]
                self.stdout.write(self.style.WARNING(f'🗑️ Deleted {deleted_count} existing records'))

            # Load data into database
            self.stdout.write('📊 Loading data into database...')
            self.load_data_to_db(data)
            
            # Show final statistics
            total_records = DeviceData.objects.count()
            self.stdout.write(self.style.SUCCESS(f'🎯 Total records in database: {total_records}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            raise CommandError(f'Command failed: {str(e)}')

    def load_data_to_db(self, data):
        """Load data into database with ranking"""
        created_count = 0
        updated_count = 0
        error_count = 0

        # Process in batches for better performance
        batch_size = 100
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            
            with transaction.atomic():
                for record in batch:
                    try:
                        # Parse date and time
                        hearttime_date = None
                        hearttime_time = None
                        
                        if record.get('hearttime_date'):
                            try:
                                hearttime_date = datetime.strptime(record['hearttime_date'], '%Y-%m-%d').date()
                            except ValueError:
                                pass
                        
                        if record.get('hearttime_time'):
                            try:
                                hearttime_time = datetime.strptime(record['hearttime_time'], '%H:%M:%S').time()
                            except ValueError:
                                pass

                        # Create or update device data
                        # Note: ranking_id is AutoField and will be assigned automatically
                        device_data, created = DeviceData.objects.update_or_create(
                            imei=record.get('imei'),
                            defaults={
                                'latitude': Decimal(str(record.get('latitude', 0))),
                                'longitude': Decimal(str(record.get('longitude', 0))),
                                'coordinates': record.get('coordinates', ''),
                                'datastatus': int(record.get('datastatus', 0)),
                                'datastatus_description': record.get('datastatus_description', ''),
                                'hearttime_date': hearttime_date,
                                'hearttime_time': hearttime_time,
                                'hearttime_unix': int(record.get('hearttime_unix', 0)),
                                'status': record.get('status', ''),
                            }
                        )
                        
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                            
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'⚠️ Error processing record {record.get("imei", "unknown")}: {str(e)}')
                        )
            
            # Progress update
            processed = min(i + batch_size, len(data))
            self.stdout.write(f'📊 Processed {processed}/{len(data)} records...')

        # Final statistics
        self.stdout.write(self.style.SUCCESS(f'✅ Created: {created_count} records'))
        self.stdout.write(self.style.SUCCESS(f'🔄 Updated: {updated_count} records'))
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠️ Errors: {error_count} records'))