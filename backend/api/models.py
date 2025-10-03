from django.db import models

# Create your models here.

class DeviceData(models.Model):
    ranking_id = models.AutoField(primary_key=True)  # Custom primary key for ranking
    imei = models.CharField(max_length=20, unique=True)  # IMEI numbers are usually 15 digits
    latitude = models.DecimalField(max_digits=9, decimal_places=6)   # precise for GPS
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    coordinates = models.CharField(max_length=50)  # storing as string "lat,long"
    
    datastatus = models.IntegerField()  
    datastatus_description = models.CharField(max_length=50)
    
    hearttime_date = models.DateField(null=True, blank=True)
    hearttime_time = models.TimeField(null=True, blank=True)
    hearttime_unix = models.BigIntegerField()  # Unix timestamp
    
    status = models.CharField(max_length=20)

    # Store relative time fields in database (optional - for faster queries)
    last_update_relative_db = models.CharField(max_length=50, blank=True, default='')  # e.g., "1 year ago"
    last_update_detailed_db = models.CharField(max_length=100, blank=True, default='')  # e.g., "365d12h30min ago"
    relative_time_calculated_at = models.DateTimeField(null=True, blank=True)  # When it was last calculated

    created_at = models.DateTimeField(auto_now_add=True)  # optional, track when saved
    updated_at = models.DateTimeField(auto_now=True)      # optional, track updates

    class Meta:
        ordering = ['ranking_id']

    def __str__(self):
        return f"IMEI: {self.imei} - {self.status}"
    
    @property
    def last_update_relative(self):
        """Get human-friendly relative time since last GPS update"""
        from .views import get_relative_time_from_unix
        return get_relative_time_from_unix(self.hearttime_unix)
    
    @property
    def last_update_detailed(self):
        """Get detailed relative time since last GPS update (e.g., 1y27d3h ago)"""
        from .views import get_detailed_relative_time_from_unix
        return get_detailed_relative_time_from_unix(self.hearttime_unix)
