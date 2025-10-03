import os
import sys
import django
import csv
import json
import shutil
import glob
from datetime import datetime
from collections import defaultdict

# Add the parent directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protrack.settings')
django.setup()

from django.conf import settings

def cleanup_old_tracking_runs(response_logs_dir, keep_latest=3):
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
                print(f"🗑️  Removed old tracking folder: {os.path.basename(folder)}")
            except Exception as e:
                print(f"⚠️  Warning: Could not remove {folder}: {e}")
                
    except Exception as e:
        print(f"⚠️  Warning: Error during cleanup: {e}")

def create_run_folder():
    """Create a timestamped folder for this run and cleanup old ones"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    response_logs_dir = os.path.join(settings.BASE_DIR, 'response_logs')
    run_folder = os.path.join(response_logs_dir, f'tracking_run_{timestamp}')
    
    # Create directories
    os.makedirs(run_folder, exist_ok=True)
    os.makedirs(response_logs_dir, exist_ok=True)
    
    # Clean up old tracking runs (keep latest 3)
    cleanup_old_tracking_runs(response_logs_dir, keep_latest=3)
    
    return run_folder, timestamp

def save_data_files(data, run_folder, fieldnames):
    """Save data to various CSV and JSON files"""
    # Save full JSON
    json_filename = os.path.join(run_folder, "all_records.json")
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSON saved to {json_filename}")
    
    # Save full CSV
    csv_filename = os.path.join(run_folder, "all_records.csv")
    with open(csv_filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({
                field: row.get(field, "") for field in fieldnames
            })
    print(f"CSV saved to {csv_filename}")
    
    return json_filename, csv_filename

def main():
    """Main function to run the tracking data collection"""
    try:
        # Import here after Django setup
        from scripts.utils.load_imei import get_imeis_from_csv
        from api.services.protrack_service import get_token, get_track_info, process_tracking_data
        
        print("=" * 50)
        print("🚀 Starting ProTrack365 Data Collection")
        print("=" * 50)
        
        # Step 1: Load IMEIs and get token
        print("\n📋 Step 1: Loading IMEIs and getting token...")
        imeis = get_imeis_from_csv()
        print(f"✅ Loaded {len(imeis)} IMEIs from MAIN.csv")
                
        token = get_token()
        print("✅ Successfully obtained authentication token")
        
        # Step 2: Fetch tracking data from API
        print("\n🌐 Step 2: Fetching tracking data from API...")
        endpoint = "https://api.protrack365.com/api/track"
        raw_data = get_track_info(imei_list=imeis, token=token, endpoint=endpoint)
        print(f"✅ Fetched {len(raw_data)} batches from API")
        
        # Step 3: Process raw data
        print("\n⚙️ Step 3: Processing raw data...")
        data = process_tracking_data(raw_data, imeis)
        print(f"✅ Processed {len(data)} total records")
        
        if data:
            print(f"📊 Sample record: {data[0]}")
        
        # Step 4: Create folder for this run
        print("\n📁 Step 4: Creating run folder...")
        run_folder, timestamp = create_run_folder()
        print(f"✅ Created run folder: {run_folder}")
        
        # Step 5: Save data files
        print("\n💾 Step 5: Saving data files...")
        fieldnames = ["imei", "latitude", "longitude", "coordinates", "datastatus", "datastatus_description", "hearttime_date", "hearttime_time", "status"]
        json_filename, csv_filename = save_data_files(data, run_folder, fieldnames)
        
        return {
            'success': True,
            'data': data,
            'run_folder': run_folder,
            'files': {
                'json': json_filename,
                'csv': csv_filename,
            }
        }
        
    except Exception as e:
        print(f"\n❌ Error in main(): {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'data': None
        }

if __name__ == "__main__":
    result = main()
    if result['success']:
        print("\n✅ Data collection completed successfully!")
        print(f"Run folder: {result['run_folder']}")
        print(f"JSON file: {result['files']['json']}")
        print(f"CSV file: {result['files']['csv']}")
    else:
        print("\n❌ Data collection failed!")
        print(f"Error: {result['error']}")