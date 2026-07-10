import requests
def get_url():
    url=input("Enter the URL: ").strip()
    if(url.startswith("https://")): # Consider handling both http:// and https:// URLs in a future revision.
        return url
    return "https://"+url 

def fetch_page(url):
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def display_response_info(response):
    print(response.status_code)
    print(len(response.content))
    print(response.headers)

def main():
    url = get_url()
    response = fetch_page(url)
    if response:
        display_response_info(response)
    else:
        print("Failed to fetch page")

if __name__ == "__main__":
    main()
    