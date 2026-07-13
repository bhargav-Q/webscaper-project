from fetcher import get_url, fetch_page, display_response_info
from analyser import analyse_html, classify_website, detect_dynamic_content

def main():
    url = get_url()
    response = fetch_page(url)
    if response:            
        display_response_info(response)
        report = analyse_html(response.text)
        print(report)
        # classify_website(response.text)
        print(detect_dynamic_content(response.text))
    else:
        print("Failed to fetch page")

if __name__ == "__main__":
    main()