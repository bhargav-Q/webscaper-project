import logging
import requests
import config
from constants import DEFAULT_SCHEME, SUPPORTED_SCHEMES

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_url():
    url = input("Enter the URL: ").strip()
    if any(url.startswith(scheme) for scheme in SUPPORTED_SCHEMES): 
        return url
    return DEFAULT_SCHEME + url 

def fetch_page(url):
    # Fetch Bright Data API credentials and settings from config
    brightdata_token = config.BRIGHTDATA_API_TOKEN
    api_url = config.BRIGHTDATA_API_URL

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {brightdata_token}"
    }

    payload = {
        "zone": config.BRIGHTDATA_ZONE,
        "url": url,
        "format": config.DEFAULT_PAYLOAD_FORMAT
    }

    try:
        response = requests.post(
            api_url, 
            headers=headers, 
            json=payload, 
            timeout=config.BRIGHTDATA_REQUEST_TIMEOUT
        )
        response.encoding = config.DEFAULT_CHARSET
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching page: %s", e)
        return None
        
def display_response_info(response):
    if response:
        logger.info("status_code: %s", response.status_code)
        logger.info("content_length: %s bytes", len(response.content))

