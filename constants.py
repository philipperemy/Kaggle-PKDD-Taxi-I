
# default value for N/A, NaN cases
NA_VALUE = -1

# Bug: it's okay if there is 8 hours of lag. The problem is the same.
# Default value in hours between Tokyo (UTC+9) and Lisbon (UTC+1)
UTC_LAG_BETWEEN_TOKYO_AND_LISBON = 0 #hours

# Name of the training file (relative location)
TRAIN_CSV_FILE_NAME = "data/train2.csv"

# Name of the testing file (relative location)
TEST_CSV_FILE_NAME = "data/test.csv"

# Max speed limit in Km/h before discarding the row
MAX_SPEED_LIMIT_BEFORE_DISCARDING = 130

# Max duration for a drive (in seconds)
MAX_DURATION_BEFORE_DISCARDING = 3600 * 2 # 2 hours

# In Poly files
LAT_ID = 0
LONG_ID = 1

TAXI_ID = 'TAXI_ID'
ORIGIN_CALL = 'ORIGIN_CALL'
ORIGIN_STAND = 'ORIGIN_STAND'
DAY_TYPE = 'DAY_TYPE'
CALL_TYPE = 'CALL_TYPE'
TRIP_ID = 'TRIP_ID'
POLYLINE = 'POLYLINE'
MISSING_DATA = 'MISSING_DATA'
TIMESTAMP = 'TIMESTAMP'
SPEED = 'SPEED'
LAST_SPEED = 'LAST_SPEED'
LAST_LAST_SPEED = 'LAST_LAST_SPEED'
DURATION = 'DURATION'
