# Direct SQL commands to clear data
# Connect to PostgreSQL and run:

# To delete all records from the DeviceData table:
# DELETE FROM api_devicedata;

# To reset the auto-increment ID counter:
# ALTER SEQUENCE api_devicedata_id_seq RESTART WITH 1;

# To truncate the table (faster for large datasets):
# TRUNCATE TABLE api_devicedata RESTART IDENTITY;

# Note: Replace 'api_devicedata' with the actual table name if different