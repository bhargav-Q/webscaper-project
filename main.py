from fetcher import get_url, fetch_page, display_response_info
from analyser import analyse_html, detect_dynamic_content

def main():
    url = get_url()
    response = fetch_page(url)
    
    # Bug 2 Fix: Safely check if the request was actually successful (200 OK)
    if response and response.status_code == 200:            
        display_response_info(response)
        report = analyse_html(response.text)
        print(report)
        print(detect_dynamic_content(response.text))
    else:
        print(f"Failed to fetch page. Status code: {response.status_code if response else 'Network Error'}")

if __name__ == "__main__":
    main()