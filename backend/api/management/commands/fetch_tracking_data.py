import os
import csv
import json
import shutil
import glob
from datetime import datetime
from collections import defaultdict

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetch tracking data from ProTrack365 API for all IMEIs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--imei-file',
            type=str,
            default='MAIN.csv',
            help='CSV file containing IMEIs (default: MAIN.csv)',

        )
        parser.add_argument(
            '--save-to',
            type=str,
            help='Custom folder name to save results (default: auto-generated timestamp)',
        )
        
    def handle(self, *args, **options):
        try:
            # Import services
            from scripts.utils.load_imei import get_imeis_from_csv
            from api.services.protrack_service import get_token, get_track_info, process_tracking_data
            
            self.stdout.write(self.style.SUCCESS('🚀 Starting ProTrack365 Data Collection'))
            
            # Step 1: Load IMEIs and get token
            self.stdout.write('📋 Loading IMEIs and getting token...')
            imeis = get_imeis_from_csv(options['imei_file'])
            self.stdout.write(self.style.SUCCESS(f'✅ Loaded {len(imeis)} IMEIs'))
            
            token = get_token()
            self.stdout.write(self.style.SUCCESS('✅ Authentication token obtained'))
            
            # Step 2: Fetch tracking data
            self.stdout.write('🌐 Fetching tracking data from API...')
            endpoint = "https://api.protrack365.com/api/track"
            raw_data = get_track_info(imei_list=imeis, token=token, endpoint=endpoint)
            self.stdout.write(self.style.SUCCESS(f'✅ Fetched {len(raw_data)} batches'))
            
            # Step 3: Process data
            self.stdout.write('⚙️ Processing raw data...')
            data = process_tracking_data(raw_data, imeis)
            self.stdout.write(self.style.SUCCESS(f'✅ Processed {len(data)} records'))
            
            # Step 4: Save results
            run_folder = self.create_run_folder(options['save_to'])
            self.stdout.write(f'📁 Saving to: {run_folder}')
            
            self.save_all_data(data, imeis, run_folder)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            raise CommandError(f'Command failed: {str(e)}')

    def cleanup_old_tracking_runs(self, response_logs_dir, keep_latest=3):
        """Remove old tracking_run folders, keeping only the latest N folders"""
        try:
            # Get all tracking_run folders
            tracking_folders = glob.glob(os.path.join(response_logs_dir, 'tracking_run_*'))
            
            if len(tracking_folders) <= keep_latest:
                return  # Nothing to clean up
            
            # Sort by modification time (newest first)
            tracking_folders.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            
            # Remove folders beyond the keep_latest count
            folders_to_remove = tracking_folders[keep_latest:]
            
            for folder in folders_to_remove:
                try:
                    shutil.rmtree(folder)
                    self.stdout.write(f'🗑️  Removed old tracking folder: {os.path.basename(folder)}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠️  Could not remove {folder}: {e}'))
                    
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Error during cleanup: {e}'))

    def create_run_folder(self, custom_name=None):
        """Create timestamped folder for results and cleanup old ones"""
        if custom_name:
            folder_name = custom_name
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            folder_name = f'tracking_run_{timestamp}'
        
        response_logs_dir = os.path.join(settings.BASE_DIR, 'response_logs')
        run_folder = os.path.join(response_logs_dir, folder_name)
        
        # Create directories
        os.makedirs(run_folder, exist_ok=True)
        os.makedirs(response_logs_dir, exist_ok=True)
        
        # Clean up old tracking runs (keep latest 3)
        self.cleanup_old_tracking_runs(response_logs_dir, keep_latest=3)
        
        return run_folder

    def save_all_data(self, data, imeis, run_folder):
        """Save all data files and return statistics"""
        # Updated fieldnames to include hearttime_unix
        fieldnames = [
            "imei", "latitude", "longitude", "coordinates", 
            "datastatus", "datastatus_description", 
            "hearttime_date", "hearttime_time",
            "hearttime_unix", "status"
        ]
         
        # Save JSON and CSV
        self.save_main_files(data, run_folder, fieldnames)
                    
    def save_main_files(self, data, run_folder, fieldnames):
        """Save main JSON and CSV files"""
        # JSON
        json_filename = os.path.join(run_folder, "all_records.json")
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # CSV
        csv_filename = os.path.join(run_folder, "all_records.csv")
        with open(csv_filename, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow({field: row.get(field, "") for field in fieldnames})
        
        self.stdout.write(f'💾 Saved: {os.path.basename(json_filename)} & {os.path.basename(csv_filename)}')
    