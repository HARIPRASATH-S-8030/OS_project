"""
Configuration file for Policy Engine
"""

# Authentication Policy
MAX_FAILED_ATTEMPTS = 3

# Time Policy (seconds)
DEFAULT_EXPIRY_TIME = 60

# View Policy
DEFAULT_VIEW_LIMIT = 1

# Backend executable
BACKEND_EXECUTABLE = "../src/backend/loader.exe"

# Logging
LOG_FILE = "policy_engine.log"