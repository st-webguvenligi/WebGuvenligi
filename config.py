#!/usr/bin/env python3
"""
WebGuvenligi Configuration
"""

import os
from pathlib import Path

# Application Info
APP_NAME = "WebGuvenligi"
APP_VERSION = "1.0.0"
APP_AUTHOR = "ST"
APP_DESCRIPTION = "Advanced Web Security Scanner"

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Scanner Settings
DEFAULT_TIMEOUT = 10
DEFAULT_THREADS = 5
DEFAULT_RETRIES = 3

# Payload Settings
MAX_PAYLOADS_PER_TYPE = 50
PAYLOAD_ENCODING = 'utf-8'

# Request Settings
DEFAULT_USER_AGENT = "WebGuvenligi/1.0 Security Scanner"
REQUEST_HEADERS = {
    'User-Agent': DEFAULT_USER_AGENT,
    'X-Scanner': 'WebGuvenligi',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Detection Settings
TIME_THRESHOLD = 2  # seconds
RESPONSE_DIFF_THRESHOLD = 0.5  # 50% difference

# Severity Levels
SEVERITY_LEVELS = ['Critical', 'High', 'Medium', 'Low', 'Info']

# Vulnerability Patterns
SQL_ERROR_PATTERNS = [
    r'sql syntax',
    r'mysql_fetch',
    r'warning.*mysql',
    r'mysql_num_rows',
    r'sql_error',
    r'fatal error',
    r'exception in',
    r'database error',
    r'syntax error',
]

# WAF Detection
WAF_SIGNATURES = [
    'CloudFlare',
    'mod_security',
    'Fortinet',
    'AWS WAF',
    'Imperva',
]
