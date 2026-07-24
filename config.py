import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# App Metadata
APP_TITLE = "Web Scraper API"
APP_VERSION = "2.0.0"

# CORS Allowed Origins
DEFAULT_ORIGINS = "http://localhost:5173,http://localhost:3000"
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", DEFAULT_ORIGINS)
ALLOWED_ORIGINS = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

# Bright Data API Settings
BRIGHTDATA_API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN", "")
BRIGHTDATA_API_URL = os.getenv("BRIGHTDATA_API_URL", "https://api.brightdata.com/request")
BRIGHTDATA_ZONE = os.getenv("BRIGHTDATA_ZONE", "web_unlocker1")
BRIGHTDATA_REQUEST_TIMEOUT = int(os.getenv("BRIGHTDATA_REQUEST_TIMEOUT", "60"))
DEFAULT_PAYLOAD_FORMAT = "raw"
DEFAULT_CHARSET = "utf-8"
