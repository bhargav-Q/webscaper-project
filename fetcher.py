import os
import requests
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def get_url():
    url = input("Enter the URL: ").strip()
    if(url.startswith("https://")): 
        return url
    return "https://"+url 

def fetch_page(url):
    # Fetch your exact API token from the .env file
    brightdata_token = os.getenv("BRIGHTDATA_API_TOKEN")
    
    # 1. The Bright Data API Endpoint
    api_url = "https://api.brightdata.com/request"

    # 2. The Headers (telling them who you are)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {brightdata_token}"
    }

    # 3. The Payload (telling them what to scrape)
    payload = {
        "zone": "web_unlocker1", # This must match the zone name in your screenshot exactly
        "url": url,
        "format": "raw"
    }

    try:
        # Notice this is a POST request now!
        response = requests.post(
            api_url, 
            headers=headers, 
            json=payload, 
            timeout=30 # Web unlocker can take time to solve CAPTCHAs
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None
        
def display_response_info(response):
    print(response.status_code)
    print(len(response.content))
