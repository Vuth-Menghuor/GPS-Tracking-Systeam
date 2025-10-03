from django.contrib import admin
from .models import DeviceData


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = [
        'ranking_id', 
        'imei', 
        'latitude', 
        'longitude', 
        'datastatus_description',
        'hearttime_date',
        'hearttime_time',
        'last_update_relative_db',
        'last_update_detailed_db',
        'status'
    ]
    
    list_filter = [
        'datastatus_description',
        'status',
        'hearttime_date',
        'last_update_relative_db'
    ]
    
    search_fields = [
        'imei',
        'last_update_relative_db',
        'last_update_detailed_db'
    ]
    
    readonly_fields = [
        'ranking_id',
        'created_at',
        'updated_at',
        'relative_time_calculated_at',
        'last_update_relative',
        'last_update_detailed'
    ]
    
    list_per_page = 50
    
    fieldsets = (
        ('Device Information', {
            'fields': ('ranking_id', 'imei', 'status')
        }),
        ('GPS Data', {
            'fields': (
                'latitude', 'longitude', 'coordinates',
                'datastatus', 'datastatus_description'
            )
        }),
        ('Timing Information', {
            'fields': (
                'hearttime_date', 'hearttime_time', 'hearttime_unix',
            )
        }),
        ('Relative Time (Database Fields)', {
            'fields': (
                'last_update_relative_db', 'last_update_detailed_db',
                'relative_time_calculated_at'
            )
        }),
        ('Relative Time (Computed Properties)', {
            'fields': (
                'last_update_relative', 'last_update_detailed'
            )
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('ranking_id')