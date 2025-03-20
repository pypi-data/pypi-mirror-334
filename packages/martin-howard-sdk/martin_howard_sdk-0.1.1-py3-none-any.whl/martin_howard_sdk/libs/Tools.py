import os
import logging
from datetime import datetime
import time
import random
import string

def get_path(filename):
    path = os.path.abspath(filename)
    return path

def log(str):
    logger = logging.getLogger(__name__)
    logger.error(str)

def traceId():
    timestamp = str(int(time.time() * 1000))  # milliseconds
    random_str = ''.join(random.choices(string.hexdigits.lower(), k=16))
    return f"{timestamp}{random_str}"

def now():
    data = datetime.now().strftime('%m/%d/%Y %I:%M %p')
    return data

US_DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'