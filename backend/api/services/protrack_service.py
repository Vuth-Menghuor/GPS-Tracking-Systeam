import hashlib
import time
import requests
import asyncio
import aiohttp
from typing import List, Dict, Any
import logging
from datetime import datetime, timezone, timedelta

# Configure logging
logger = logging.getLogger(__name__)

def get_token():
    """Get authentication token from ProTrack365 API"""
    account = "bajajtrack"
    password = "bajajrecombodia"
    unix_time = int(time.time())

    # Generate MD5 hashed password
    first_hash = hashlib.md5(password.encode()).hexdigest()
    signature = hashlib.md5((first_hash + str(unix_time)).encode()).hexdigest()

    # Build endpoint
    endpoint = f"https://api.protrack365.com/api/authorization?time={unix_time}&account={account}&signature={signature}"

    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'record' in data and 'access_token' in data['record']:
            token = data['record']['access_token']
            logger.info("Successfully obtained access token")
            return token
        else:
            logger.error(f"Invalid response format: {data}")
            raise ValueError("Invalid response format from authorization API")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching token: {e}")
        raise
    except KeyError as e:
        logger.error(f"Missing key in response: {e}")
        raise

def get_device_list(account, token):
    """Get list of devices from ProTrack365 API"""
    endpoint = f"https://api.protrack365.com/api/device/list?access_token={token}&account={account}"
    
    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Device list response: {data}")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching device list: {e}")
        raise

def chunk_list(lst: List[str], size: int = 100) -> List[List[str]]:
    """Split list into chunks of specified size"""
    return [lst[i:i + size] for i in range(0, len(lst), size)]

async def fetch_batch(session: aiohttp.ClientSession, imei_batch: List[str], token: str, endpoint: str) -> Dict[str, Any]:
    """Fetch tracking data for a batch of IMEIs"""
    params = {  
        "imeis": ",".join(imei_batch),
        "access_token": token
    }
    
    try:
        async with session.get(endpoint, params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
            response.raise_for_status()
            data = await response.json()
            logger.debug(f"Batch response for {len(imei_batch)} IMEIs: {data}")
            return data
    except Exception as e:
        logger.error(f"Error fetching batch {imei_batch[:3]}...: {e}")
        # Return error info instead of raising to continue with other batches
        return {
            "error": str(e),
            "imei_batch": imei_batch,
            "status": "failed"
        }

async def get_track_info_concurrent(imei_list: List[str], token: str, endpoint: str) -> List[Dict[str, Any]]:
    """Main async function to fetch tracking data for all IMEIs"""
    if not imei_list:
        logger.warning("Empty IMEI list provided")
        return []
    
    imei_chunks = chunk_list(imei_list, 100)
    logger.info(f"Processing {len(imei_list)} IMEIs in {len(imei_chunks)} batches")
    
    # Set up aiohttp session with proper timeout and connection limits
    timeout = aiohttp.ClientTimeout(total=120)
    connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
    
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        tasks = [
            fetch_batch(session, chunk, token, endpoint)
            for chunk in imei_chunks
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle exceptions
        successful_results = []
        failed_batches = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch {i} failed with exception: {result}")
                failed_batches.append({
                    "batch_index": i,
                    "imei_batch": imei_chunks[i],
                    "error": str(result),
                    "status": "exception"
                })
            elif isinstance(result, dict) and "error" in result:
                logger.error(f"Batch {i} returned error: {result['error']}")
                failed_batches.append(result)
            else:
                successful_results.append(result)
        
        logger.info(f"Successfully fetched {len(successful_results)} batches, {len(failed_batches)} failed")
        
        if failed_batches:
            logger.warning(f"Failed batches: {failed_batches}")
        
        return successful_results

def get_track_info(imei_list: List[str], token: str, endpoint: str) -> List[Dict[str, Any]]:
    """Synchronous wrapper to call the async tracking function"""
    try:
        # Check if we're already in an event loop
        try:
            loop = asyncio.get_running_loop()
            # If we get here, we're in an async context
            logger.warning("Already in async context, cannot use asyncio.run()")
            # In this case, you'd need to handle this differently
            # For now, we'll raise an exception
            raise RuntimeError("Cannot call asyncio.run() from within an async context")
        except RuntimeError:
            # No event loop running, safe to use asyncio.run()
            return asyncio.run(get_track_info_concurrent(imei_list, token, endpoint))
    except Exception as e:
        logger.error(f"Error in get_track_info: {e}")
        raise

def get_datastatus_description(datastatus):
    """Convert numeric datastatus to human-readable description"""
    status_map = {
        1: "Never online",
        2: "Online", 
        3: "Expired",
        4: "Offline",
        5: "Block"
    }
    try:
        return status_map.get(int(datastatus), "Unknown")
    except (ValueError, TypeError):
        return "Unknown"

def combine_coordinates(latitude, longitude):
    """Combine latitude and longitude into a single string"""
    if (latitude and longitude and 
        str(latitude) not in ["", "0", "0.0", "None", "null"] and 
        str(longitude) not in ["", "0", "0.0", "None", "null"]):
        return f"{latitude},{longitude}"
    return "0,0"

def convert_hearttime_to_gmt7_separated(unix_timestamp):
    """Convert Unix timestamp to GMT+7 and return separated date and time"""
    if not unix_timestamp or unix_timestamp in ["", "0", 0, "None", "null", None]:
        return "", ""
    
    try:
        if isinstance(unix_timestamp, str):
            unix_timestamp = int(unix_timestamp)
        # Create UTC datetime from timestamp
        utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)

        # Convert to GMT+7
        gmt7_timezone = timezone(timedelta(hours=7))
        gmt7_datetime = utc_datetime.astimezone(gmt7_timezone)

        #return separate date and time 
        date_part = gmt7_datetime.strftime("%Y-%m-%d")
        time_part = gmt7_datetime.strftime("%H:%M:%S")

        return date_part, time_part
    
    except (ValueError, TypeError, OSError) as e: 
        logger.warning(f"Error converting hearttime {unix_timestamp}: {e}")
        return str(unix_timestamp), str(unix_timestamp)


def convert_hearttime_to_gmt7(unix_timestamp):
    """Convert Unix timestamp to GMT+7 datetime string"""
    if not unix_timestamp or unix_timestamp in ["", "0", 0, "None", "null", None]:
        return ""
    
    try:
        # Convert to integer if it's a string
        if isinstance(unix_timestamp, str):
            unix_timestamp = int(unix_timestamp)
        
        # Create UTC datetime from timestamp
        utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        
        # Convert to GMT+7
        gmt7_timezone = timezone(timedelta(hours=7))
        gmt7_datetime = utc_datetime.astimezone(gmt7_timezone)
        
        # Return formatted datetime string
        return gmt7_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
    except (ValueError, TypeError, OSError) as e:
        logger.warning(f"Error converting hearttime {unix_timestamp}: {e}")
        return str(unix_timestamp)  # Return original value as string if conversion fails

def process_tracking_data(raw_data: List[Dict[str, Any]], original_imeis: List[str]) -> List[Dict[str, Any]]:
    """Process raw API response data into standardized format"""
    processed_data = []
    returned_imeis = set()
    
    for batch in raw_data:
        if isinstance(batch, dict) and 'record' in batch:
            records = batch['record']
            if not isinstance(records, list):
                records = [records]
                
            for device in records:
                if isinstance(device, dict):
                    imei = device.get('imei', '')
                    latitude = device.get('latitude', '')
                    longitude = device.get('longitude', '')
                    datastatus_num = device.get('datastatus', '')
                    raw_hearttime = device.get('hearttime', '')
                    
                    heart_date, heart_time = convert_hearttime_to_gmt7_separated(raw_hearttime)

                    processed_data.append({
                        'imei': str(imei),
                        'latitude': latitude,
                        'longitude': longitude,
                        'coordinates': combine_coordinates(latitude, longitude),
                        'datastatus': datastatus_num,
                        'datastatus_description': get_datastatus_description(datastatus_num),
                        'hearttime_date': heart_date,
                        'hearttime_time': heart_time,
                        'hearttime_unix': raw_hearttime,
                        'status': 'success'
                    })
                    
                    if imei:
                        returned_imeis.add(str(imei))
        else:
            # Handle batch errors or unexpected formats
            logger.warning(f"Unexpected batch format: {batch}")
            if isinstance(batch, dict) and "imei_batch" in batch:
                # This is a failed batch, add error records
                for imei in batch["imei_batch"]:
                    processed_data.append({
                        "imei": str(imei),
                        "latitude": "",
                        "longitude": "",
                        "coordinates": "0,0",
                        "datastatus": None,
                        "datastatus_description": "API Error",
                        "hearttime_date": "",
                        "hearttime_time": "",
                        "hearttime_unix": "",
                        "status": f"API error: {batch.get('error', 'Unknown error')}"
                    })
    
    # Add missing IMEIs as "can't access"
    missing_imeis = set(str(imei) for imei in original_imeis) - returned_imeis
    for imei in missing_imeis:
        processed_data.append({
            "imei": str(imei),
            "latitude": "",
            "longitude": "",
            "coordinates": "0,0",
            "datastatus": None,
            "datastatus_description": "No data",
            "hearttime_date": "",
            "hearttime_time": "",
            "hearttime_unix": "",
            "status": f"can't access to {imei}"
        })
    
    logger.info(f"Processed {len(processed_data)} total records")
    return processed_data