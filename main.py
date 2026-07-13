from bs4 import BeautifulSoup
import requests

def get_url():
    url = input("Enter the URL: ").strip()
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
    # print(response.headers)

def analyse_html(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    
    # Use len() around your find_all() calls to get the counts!
    report = {
        "title": soup.title.text if soup.title else "No Title",
        "h1": len(soup.find_all('h1')),
        "h2": len(soup.find_all('h2')),
        "h3": len(soup.find_all('h3')),
        "links": len(soup.find_all('a')),
        "images": len(soup.find_all('img')),
        "tables": len(soup.find_all('table')),
        "forms": len(soup.find_all('form'))
    }
    
    return report

def main():
    url = get_url()
    response = fetch_page(url)
    if response:
        display_response_info(response)
        report = analyse_html(response.text)
        print(report) 
    else:
        print("Failed to fetch page")

if __name__ == "__main__":
    main()