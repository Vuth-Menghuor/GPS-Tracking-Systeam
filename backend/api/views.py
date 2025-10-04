from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.core.management import call_command
from django.conf import settings
from django.utils import timezone
import json
import csv
import os
import subprocess
from datetime import datetime, timedelta
from .models import DeviceData


def get_relative_time(target_date):
    """Calculate relative time from target_date to now"""
    if not target_date:
        return "Never"
    
    # Get current date
    now = timezone.now().date()
    
    # Convert target_date to date if it's datetime
    if hasattr(target_date, 'date'):
        target_date = target_date.date()
    
    # Calculate difference
    diff = now - target_date
    days = diff.days
    
    if days == 0:
        return "Today"
    elif days == 1:
        return "1 day ago"
    elif days < 7:
        return f"{days} days ago"
    elif days < 30:
        weeks = days // 7
        remaining_days = days % 7
        if weeks == 1:
            if remaining_days == 0:
                return "1 week ago"
            else:
                return f"1w {remaining_days}d ago"
        else:
            if remaining_days == 0:
                return f"{weeks} weeks ago"
            else:
                return f"{weeks}w {remaining_days}d ago"
    elif days < 365:
        months = days // 30
        remaining_days = days % 30
        if months == 1:
            if remaining_days == 0:
                return "1 month ago"
            else:
                return f"1m {remaining_days}d ago"
        else:
            if remaining_days == 0:
                return f"{months} months ago"
            else:
                return f"{months}m {remaining_days}d ago"
    else:
        years = days // 365
        remaining_days = days % 365
        if years == 1:
            if remaining_days == 0:
                return "1 year ago"
            elif remaining_days < 30:
                return f"1y {remaining_days}d ago"
            else:
                months = remaining_days // 30
                return f"1y {months}m ago"
        else:
            if remaining_days == 0:
                return f"{years} years ago"
            elif remaining_days < 30:
                return f"{years}y {remaining_days}d ago"
            else:
                months = remaining_days // 30
                return f"{years}y {months}m ago"


def get_detailed_relative_time(target_date):
    """Get detailed relative time like '365d12h30min ago'"""
    if not target_date:
        return "Never"
    
    # Convert to datetime if it's a date
    if hasattr(target_date, 'date') and not hasattr(target_date, 'hour'):
        # It's a date object, convert to datetime at midnight
        target_datetime = datetime.combine(target_date, datetime.min.time())
        target_datetime = timezone.make_aware(target_datetime)
    else:
        target_datetime = target_date
        if not timezone.is_aware(target_datetime):
            target_datetime = timezone.make_aware(target_datetime)
    
    # Get current datetime
    now = timezone.now()
    
    # Calculate difference
    diff = now - target_datetime
    total_seconds = int(diff.total_seconds())
    
    if total_seconds < 0:
        return "In the future"
    elif total_seconds < 60:
        return f"{total_seconds}s ago"
    elif total_seconds < 3600:  # Less than 1 hour
        minutes = total_seconds // 60
        return f"{minutes}min ago"
    elif total_seconds < 86400:  # Less than 1 day
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if minutes == 0:
            return f"{hours}h ago"
        else:
            return f"{hours}h{minutes}min ago"
    else:  # 1 day or more
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        
        if days < 365:
            if hours == 0:
                return f"{days}d ago"
            elif minutes == 0:
                return f"{days}d{hours}h ago"
            else:
                return f"{days}d{hours}h{minutes}min ago"
        else:
            years = days // 365
            remaining_days = days % 365
            if remaining_days == 0:
                return f"{years}y ago"
            else:
                return f"{years}y{remaining_days}d ago"


def get_detailed_relative_time_from_unix(unix_timestamp):
    """Get detailed relative time from Unix timestamp - REAL-TIME calculation"""
    if not unix_timestamp or unix_timestamp == 0:
        return "Never"
    
    try:
        # Convert Unix timestamp to datetime
        from datetime import timezone as dt_timezone
        target_datetime = datetime.fromtimestamp(unix_timestamp, tz=dt_timezone.utc)
        
        # Get current datetime
        now = timezone.now()
        
        # Calculate difference
        diff = now - target_datetime
        total_seconds = int(diff.total_seconds())
        
        if total_seconds < -86400:  # More than 1 day in future
            return "Future timestamp"
        elif total_seconds < 0:
            return "In near future"
        elif total_seconds < 60:
            return f"{total_seconds}s ago"
        elif total_seconds < 3600:  # Less than 1 hour
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}min{seconds}s ago"
        elif total_seconds < 86400:  # Less than 1 day
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h{minutes}min ago"
        else:  # 1 day or more
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            
            if days < 365:
                if hours == 0 and minutes == 0:
                    return f"{days}d ago"
                elif minutes == 0:
                    return f"{days}d{hours}h ago"
                else:
                    return f"{days}d{hours}h{minutes}min ago"
            else:
                years = days // 365
                remaining_days = days % 365
                remaining_hours = (total_seconds % 86400) // 3600
                if remaining_days == 0:
                    return f"{years}y ago"
                elif remaining_hours == 0:
                    return f"{years}y{remaining_days}d ago"
                else:
                    return f"{years}y{remaining_days}d{remaining_hours}h ago"
                    
    except (ValueError, TypeError, OSError) as e:
        return "Invalid timestamp"


def get_relative_time_from_unix(unix_timestamp):
    """Get human-friendly relative time from Unix timestamp - REAL-TIME calculation"""
    if not unix_timestamp or unix_timestamp == 0:
        return "Never"
    
    try:
        # Convert Unix timestamp to datetime
        from datetime import timezone as dt_timezone
        target_datetime = datetime.fromtimestamp(unix_timestamp, tz=dt_timezone.utc)
        
        # Get current datetime
        now = timezone.now()
        
        # Calculate difference
        diff = now - target_datetime
        total_seconds = int(diff.total_seconds())
        days = abs(total_seconds) // 86400  # Use absolute value for calculations
        
        if total_seconds < -86400:  # More than 1 day in future
            return "Future timestamp"
        elif total_seconds < 0:  # Future but less than a day
            return "In near future"
        elif total_seconds < 3600:  # Less than 1 hour
            minutes = total_seconds // 60
            return f"{minutes} min ago" if minutes > 0 else "Just now"
        elif total_seconds < 86400:  # Less than 1 day
            hours = total_seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif days == 1:
            return "1 day ago"
        elif days < 7:
            return f"{days} days ago"
        elif days < 30:
            weeks = days // 7
            remaining_days = days % 7
            if weeks == 1:
                return f"1 week ago" if remaining_days == 0 else f"1w {remaining_days}d ago"
            else:
                return f"{weeks} weeks ago" if remaining_days == 0 else f"{weeks}w {remaining_days}d ago"
        elif days < 365:
            months = days // 30
            remaining_days = days % 30
            if months == 1:
                return f"1 month ago" if remaining_days == 0 else f"1m {remaining_days}d ago"
            else:
                return f"{months} months ago" if remaining_days == 0 else f"{months}m {remaining_days}d ago"
        else:
            years = days // 365
            remaining_days = days % 365
            if years == 1:
                if remaining_days == 0:
                    return "1 year ago"
                elif remaining_days < 30:
                    return f"1y {remaining_days}d ago"
                else:
                    months = remaining_days // 30
                    return f"1y {months}m ago"
            else:
                if remaining_days == 0:
                    return f"{years} years ago"
                elif remaining_days < 30:
                    return f"{years}y {remaining_days}d ago"
                else:
                    months = remaining_days // 30
                    return f"{years}y {months}m ago"
                    
    except (ValueError, TypeError, OSError) as e:
        return "Invalid timestamp"


@csrf_exempt
@require_http_methods(["GET"])
def get_device_data(request):
    """Get paginated device data"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 50))
        
        # Get all device data ordered by ranking_id
        devices = DeviceData.objects.all().order_by('ranking_id')
        
        # Paginate
        paginator = Paginator(devices, per_page)
        page_obj = paginator.get_page(page)
        
        # Convert to list of dictionaries
        data = []
        for device in page_obj:
            data.append({
                'ranking_id': device.ranking_id,
                'imei': device.imei,
                'latitude': float(device.latitude),
                'longitude': float(device.longitude),
                'coordinates': device.coordinates,
                'datastatus': device.datastatus,
                'datastatus_description': device.datastatus_description,
                'hearttime_date': device.hearttime_date.strftime('%Y-%m-%d') if device.hearttime_date else '',
                'hearttime_time': device.hearttime_time.strftime('%H:%M:%S') if device.hearttime_time else '',
                'hearttime_unix': device.hearttime_unix,
                'status': device.status,
                'created_at': device.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': device.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                # Add REAL-TIME relative time fields using model properties
                'last_update_relative': device.last_update_relative,
                'last_update_detailed': device.last_update_detailed,
            })
        
        return JsonResponse({
            'success': True,
            'data': data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_records': paginator.count,
                'per_page': per_page,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def fetch_tracking_data(request):
    """Fetch new GPS tracking data from API"""
    try:
        import traceback
        
        # Run the management command
        call_command('fetch_tracking_data')
        
        # Get the latest response log folder
        response_logs_dir = os.path.join(settings.BASE_DIR, 'response_logs')
        if os.path.exists(response_logs_dir):
            folders = [f for f in os.listdir(response_logs_dir) if f.startswith('tracking_run_')]
            if folders:
                latest_folder = sorted(folders)[-1]
                json_file = os.path.join(response_logs_dir, latest_folder, 'all_records.json')
                
                return JsonResponse({
                    'success': True,
                    'message': 'GPS tracking data fetched successfully',
                    'json_file': json_file,
                    'folder': latest_folder
                })
        
        return JsonResponse({
            'success': True,
            'message': 'GPS tracking data fetched successfully',
            'json_file': None
        })
        
    except Exception as e:
        import traceback
        error_details = {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }
        return JsonResponse({
            'success': False, 
            'error': str(e),
            'details': error_details
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def load_to_database(request):
    """Load JSON data to database"""
    try:
        data = json.loads(request.body)
        json_file = data.get('json_file')
        clear_existing = data.get('clear_existing', False)
        
        if not json_file or not os.path.exists(json_file):
            return JsonResponse({'success': False, 'error': 'JSON file not found'}, status=400)
        
        # Build command arguments
        cmd_args = ['load_device_data', json_file]
        if clear_existing:
            cmd_args.append('--clear-existing')
        
        # Run the management command
        call_command(*cmd_args)
        
        # Get updated statistics
        total_records = DeviceData.objects.count()
        
        return JsonResponse({
            'success': True,
            'message': f'Data loaded successfully. Total records: {total_records}',
            'total_records': total_records
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def export_to_csv(request):
    """Export all device data to CSV"""
    try:
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="gps_tracking_data_{timestamp}.csv"'
        
        # Create CSV writer
        writer = csv.writer(response)
        
        # Write header with new relative time columns
        writer.writerow([
            'Ranking ID', 'IMEI', 'Latitude', 'Longitude', 'Coordinates',
            'Data Status Code', 'Data Status', 'Heart Date', 'Heart Time',
            'Heart Unix', 'Status', 'Created At', 'Updated At',
            'Last Update Relative', 'Last Update Detailed'
        ])
        
        # Write data with real-time relative timestamps
        devices = DeviceData.objects.all().order_by('ranking_id')
        for device in devices:
            writer.writerow([
                device.ranking_id,
                device.imei,
                device.latitude,
                device.longitude,
                device.coordinates,
                device.datastatus,
                device.datastatus_description,
                device.hearttime_date.strftime('%Y-%m-%d') if device.hearttime_date else '',
                device.hearttime_time.strftime('%H:%M:%S') if device.hearttime_time else '',
                device.hearttime_unix,
                device.status,
                device.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                device.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                # Add real-time relative timestamps to CSV export using model properties
                device.last_update_relative,
                device.last_update_detailed,
            ])
        
        return response
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_stats(request):
    """Get dashboard statistics"""
    try:
        total_devices = DeviceData.objects.count()
        
        # Status counts
        status_counts = {}
        for status in DeviceData.objects.values_list('datastatus_description', flat=True).distinct():
            count = DeviceData.objects.filter(datastatus_description=status).count()
            status_counts[status] = count
        
        # GPS coordinates availability
        with_coordinates = DeviceData.objects.exclude(latitude=0, longitude=0).count()
        without_coordinates = total_devices - with_coordinates
        
        return JsonResponse({
            'success': True,
            'stats': {
                'total_devices': total_devices,
                'with_coordinates': with_coordinates,
                'without_coordinates': without_coordinates,
                'status_counts': status_counts
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_recent_logs(request):
    """Get list of recent tracking runs"""
    try:
        response_logs_dir = os.path.join(settings.BASE_DIR, 'response_logs')
        logs = []
        
        if os.path.exists(response_logs_dir):
            folders = [f for f in os.listdir(response_logs_dir) if f.startswith('tracking_run_')]
            folders.sort(reverse=True)  # Most recent first
            
            for folder in folders[:10]:  # Get last 10 runs
                folder_path = os.path.join(response_logs_dir, folder)
                json_file = os.path.join(folder_path, 'all_records.json')
                
                if os.path.exists(json_file):
                    # Get file size and modification time
                    stat = os.stat(json_file)
                    size_mb = round(stat.st_size / (1024 * 1024), 2)
                    mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    
                    logs.append({
                        'folder': folder,
                        'json_file': json_file,
                        'size_mb': size_mb,
                        'modified': mod_time
                    })
        
        return JsonResponse({
            'success': True,
            'logs': logs
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)