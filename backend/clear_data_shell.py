# You can also clear data using Django shell
# Run: python manage.py shell
# Then execute:

from api.models import DeviceData

# Count current records
print(f"Current records: {DeviceData.objects.count()}")

# Delete all records
DeviceData.objects.all().delete()

# Confirm deletion
print(f"Records after deletion: {DeviceData.objects.count()}")