import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import DOMAnalyzer, EntityDetector

# The structural tags that define major "sections" of a webpage
SECTION_TAGS = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer', 'table']

def get_dom_stats(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    analyzer = DOMAnalyzer(soup)
    return analyzer.get_stats()


def scan_sections(html_text):
    """
    Step 1 of the Two-Step Flow.
    Scans the rendered HTML and identifies the major structural sections.
    Returns a list of section previews for the React frontend to display.
    """
    soup = BeautifulSoup(html_text, 'lxml')
    sections = []
    section_index = 0

    # 1. Look for semantic HTML5 elements (header, nav, main, section, etc.)
    for tag in soup.find_all(SECTION_TAGS):
        preview_text = tag.get_text(separator=' ', strip=True)[:150]
        if not preview_text:
            continue

        section_id = f"section-{section_index}"
        tag['data-scraper-id'] = section_id
        
        sections.append({
            "section_id": section_id,
            "tag": tag.name,
            "class": ' '.join(tag.get('class', [])),
            "id": tag.get('id', ''),
            "preview": preview_text
        })
        section_index += 1

    # 2. Structural Grid Detection (DOM Signature Hashing) using DOMAnalyzer
    analyzer = DOMAnalyzer(soup)
    grid_nodes = analyzer.find_grids()
    
    for tag in grid_nodes:
        if 'data-scraper-id' in tag.attrs:
            continue # Already added
            
        preview_text = tag.get_text(separator=' ', strip=True)[:150]
        section_id = f"section-{section_index}"
        tag['data-scraper-id'] = section_id
        
        sections.append({
            "section_id": section_id,
            "tag": tag.name,
            "class": ' '.join(tag.get('class', [])),
            "id": tag.get('id', ''),
            "preview": preview_text
        })
        section_index += 1

    return sections, str(soup)


def _find_section_element(soup, section_info):
    """
    Helper function that finds the exact HTML element matching a section preview.
    Uses the injected data-scraper-id to locate the right element flawlessly.
    """
    section_id = section_info.get("section_id")
    if section_id:
        return soup.find(attrs={"data-scraper-id": section_id})
    return None


def analyse_html(base_url, html_text, selected_sections=None):
    """
    Step 2 of the Two-Step Flow.
    Extracts data in a Relational (Grouped) format based on selected sections.
    """
    soup = BeautifulSoup(html_text, 'lxml')

    # Page Title (always from the full page)
    title = soup.title.text.strip() if soup.title else "No Title"

    # Determine which parts of the page to search
    if selected_sections:
        # Build a list of BeautifulSoup elements for only the selected sections
        search_targets = []
        for section in selected_sections:
            element = _find_section_element(soup, section)
            if element:
                search_targets.append(element)
    else:
        # If no sections selected, try to find articles, otherwise just use the body
        search_targets = soup.find_all('article')
        if not search_targets:
            search_targets = [soup.find('body') or soup]

    # Extract relational records from the target elements
    records = []
    detector = EntityDetector(base_url)

    for target in search_targets:
        # If the target is a table, use Tabular Data Extraction
        if target.name == 'table':
            headers = [th.get_text(strip=True) for th in target.find_all('th')]
            for tr in target.find_all('tr'):
                cells = tr.find_all(['td', 'th'])
                # Skip header-only rows
                if not cells or all(c.name == 'th' for c in cells): 
                    continue 
                
                record = {}
                for i, cell in enumerate(cells):
                    key = headers[i] if i < len(headers) and headers[i] else f"Column {i+1}"
                    record[key] = cell.get_text(strip=True)
                
                if any(record.values()):
                    records.append(record)
            continue

        # Otherwise, use EntityDetector for universal extraction
        record = detector.extract_entities(target)
        if any(record.values()):
            records.append(record)

    report = {
        "title": title,
        "summary": {
            "total_records": len(records)
        },
        "data": {
            "records": records
        }
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
