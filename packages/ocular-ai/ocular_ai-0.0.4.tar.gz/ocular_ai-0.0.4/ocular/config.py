"""
Default configuration for the Ocular SDK.
"""

import os

from dotenv import load_dotenv

load_dotenv()

OCULAR_API_URL = os.environ.get("OCULAR_API_URL", "https://api.useocular.com/api/v1")

OCULAR_TIMEOUT = int(os.environ.get("OCULAR_TIMEOUT", "300"))

OCULAR_MAX_RETRIES = int(os.environ.get("OCULAR_MAX_RETRIES", "3"))

OCULAR_BACKOFF_FACTOR = float(os.environ.get("OCULAR_BACKOFF_FACTOR", "0.5"))

OCULAR_DEBUG = os.environ.get("OCULAR_DEBUG", "").lower() in ("true", "1", "yes")
