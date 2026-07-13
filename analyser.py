from bs4 import BeautifulSoup


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


def detect_dynamic_content(html_text):
    if 'id="root"' in html_text or '__NEXT_DATA__' in html_text:
        return "Built with React"
    
    elif 'id="app"' in html_text or 'data-v-' in html_text:
        return "Built with Vue"
        
    elif 'ng-version' in html_text:
        return "Built with Angular"
        
    else:
        return "Static or unknown framework"
