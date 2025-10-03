import csv
import os
from django.conf import settings

def get_imeis_from_csv(filename="LATEST_IMEI.csv"):
    """
    Load IMEIs from CSV file where:
    - First column is index/number
    - Second column is TOTAL IMEI (the actual IMEI values we need)
    """
    imeis = []
    
    # Try multiple possible paths for the CSV file
    possible_paths = [
        os.path.join(settings.BASE_DIR, filename),  # Root of Django project
        os.path.join(settings.BASE_DIR, 'scripts', filename),  # In scripts directory
        os.path.join(os.path.dirname(__file__), '..', '..', filename),  # Two levels up from current file
        os.path.join(os.path.dirname(__file__), filename),  # Same directory as this file
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if csv_path is None:
        print(f"CSV file '{filename}' not found in any of these locations:")
        for path in possible_paths:
            print(f"  - {path}")
        raise FileNotFoundError(f"Could not find {filename}")
    
    print(f"Found CSV file at: {csv_path}")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            # Skip header row if it exists
            header = next(reader, None)
            print(f"CSV header: {header}")
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 because we skipped header
                if len(row) >= 2:  # Make sure we have at least 2 columns
                    imei = str(row[1]).strip()  # Second column contains the IMEI, convert to string
                    if imei and imei != "TOTAL IMEI" and imei.lower() != "total imei":  # Skip empty cells and header
                        imeis.append(imei)
                elif len(row) == 1 and row[0].strip():  # Single column case
                    imei = str(row[0]).strip()
                    if imei and not imei.startswith('#'):  # Skip comments
                        imeis.append(imei)
        
        print(f"Successfully loaded {len(imeis)} IMEIs from {csv_path}")
        if imeis:
            print(f"First few IMEIs: {imeis[:3]}")
            print(f"Last few IMEIs: {imeis[-3:]}")
        
        return imeis
        
    except Exception as e:
        print(f"Error reading file {csv_path}: {e}")
        raise

# Test function to verify the loader works
def test_imei_loader():
    """Test function to verify IMEI loading works correctly"""
    try:
        imeis = get_imeis_from_csv()
        if imeis:
            print(f"✅ Test passed: Loaded {len(imeis)} IMEIs")
            print(f"   Sample IMEIs: {imeis[:5] if len(imeis) >= 5 else imeis}")
            return True
        else:
            print("❌ Test failed: No IMEIs loaded")
            return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_imei_loader()