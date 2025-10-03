from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import DeviceData
from api.views import get_relative_time_from_unix, get_detailed_relative_time_from_unix


class Command(BaseCommand):
    help = 'Update relative time fields in database for all devices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of records to process in each batch (default: 100)',
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        
        self.stdout.write('🔄 Updating relative time fields in database...')
        
        # Get total count
        total_devices = DeviceData.objects.count()
        self.stdout.write(f'📊 Total devices to process: {total_devices}')
        
        # Process in batches
        updated_count = 0
        current_time = timezone.now()
        
        for i in range(0, total_devices, batch_size):
            batch = DeviceData.objects.all()[i:i + batch_size]
            
            # Prepare bulk update data
            devices_to_update = []
            
            for device in batch:
                # Calculate relative times
                device.last_update_relative_db = get_relative_time_from_unix(device.hearttime_unix)
                device.last_update_detailed_db = get_detailed_relative_time_from_unix(device.hearttime_unix)
                device.relative_time_calculated_at = current_time
                
                devices_to_update.append(device)
            
            # Update each device individually (more reliable than bulk_update)
            for device in devices_to_update:
                try:
                    device.save(update_fields=['last_update_relative_db', 'last_update_detailed_db', 'relative_time_calculated_at'])
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠️ Error updating device {device.imei}: {e}'))
            
            updated_count += len(devices_to_update)
            self.stdout.write(f'✅ Updated {updated_count}/{total_devices} devices...')
        
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Successfully updated relative time fields for {updated_count} devices!')
        )
        
        # Show some examples
        self.stdout.write('\n📋 Sample results:')
        sample_devices = DeviceData.objects.all()[:5]
        for device in sample_devices:
            self.stdout.write(
                f'   IMEI: {device.imei} | Relative: {device.last_update_relative_db} | Detailed: {device.last_update_detailed_db}'
            )