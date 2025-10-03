from django.core.management.base import BaseCommand
from api.models import DeviceData

class Command(BaseCommand):
    help = 'Clear all device data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            confirm = input('Are you sure you want to delete all DeviceData records? (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
                return

        # Count records before deletion
        count = DeviceData.objects.count()
        
        if count == 0:
            self.stdout.write(self.style.WARNING('No records found to delete.'))
            return

        # Delete all records
        DeviceData.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} DeviceData records.')
        )