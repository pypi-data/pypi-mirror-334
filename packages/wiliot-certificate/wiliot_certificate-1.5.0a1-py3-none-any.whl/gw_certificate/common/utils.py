
# External libraries
import datetime

# Date & Time Related
def current_timestamp():
    """returns current timestamp (UTC) in milliseconds"""
    return datetime.datetime.timestamp(datetime.datetime.now()) * 1000
