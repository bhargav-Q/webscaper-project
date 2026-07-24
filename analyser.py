import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import DOMAnalyzer, EntityDetector
from constants import (
    DEFAULT_COLUMN_PREFIX,
    DEFAULT_FRAMEWORK,
    DEFAULT_HTML_PARSER,
    DEFAULT_PAGE_TITLE,
    FALLBACK_SEARCH_TARGETS,
    FRAMEWORK_DETECTION_RULES,
    MAX_SECTION_PREVIEW_LEN,
    SCRAPER_ID_ATTR,
    SECTION_ID_PREFIX,
    SECTION_TAGS,
    TABLE_CELL_TAGS,
)

def get_dom_stats(html_text):
    soup = BeautifulSoup(html_text, DEFAULT_HTML_PARSER)
    analyzer = DOMAnalyzer(soup)
    return analyzer.get_stats()


def scan_sections(html_text):
    """
    Step 1 of the Two-Step Flow.
    Scans the rendered HTML and identifies the major structural sections.
    Returns a list of section previews for the React frontend to display.
    """
    soup = BeautifulSoup(html_text, DEFAULT_HTML_PARSER)
    sections = []
    section_index = 0

    # 1. Look for semantic HTML5 elements (header, nav, main, section, etc.)
    for tag in soup.find_all(SECTION_TAGS):
        preview_text = tag.get_text(separator=' ', strip=True)[:MAX_SECTION_PREVIEW_LEN]
        if not preview_text:
            continue

        section_id = f"{SECTION_ID_PREFIX}{section_index}"
        tag[SCRAPER_ID_ATTR] = section_id
        
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
        if SCRAPER_ID_ATTR in tag.attrs:
            continue # Already added
            
        preview_text = tag.get_text(separator=' ', strip=True)[:MAX_SECTION_PREVIEW_LEN]
        section_id = f"{SECTION_ID_PREFIX}{section_index}"
        tag[SCRAPER_ID_ATTR] = section_id
        
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
        return soup.find(attrs={SCRAPER_ID_ATTR: section_id})
    return None


def analyse_html(base_url, html_text, selected_sections=None):
    """
    Step 2 of the Two-Step Flow.
    Extracts data in a Relational (Grouped) format based on selected sections.
    """
    soup = BeautifulSoup(html_text, DEFAULT_HTML_PARSER)

    # Page Title (always from the full page)
    title = soup.title.text.strip() if soup.title else DEFAULT_PAGE_TITLE

    # Determine which parts of the page to search
    if selected_sections:
        # Build a list of BeautifulSoup elements for only the selected sections
        search_targets = []
        for section in selected_sections:
            element = _find_section_element(soup, section)
            if element:
                search_targets.append(element)
    else:
        # If no sections selected, try fallback search targets (e.g. articles or body)
        search_targets = soup.find_all(FALLBACK_SEARCH_TARGETS[0])
        if not search_targets:
            search_targets = [soup.find(FALLBACK_SEARCH_TARGETS[1]) or soup]

    # Extract relational records from the target elements
    records = []
    detector = EntityDetector(base_url)

    for target in search_targets:
        # If the target is a table, use Tabular Data Extraction
        if target.name == 'table':
            headers = [th.get_text(strip=True) for th in target.find_all('th')]
            for tr in target.find_all('tr'):
                cells = tr.find_all(TABLE_CELL_TAGS)
                # Skip header-only rows
                if not cells or all(c.name == 'th' for c in cells): 
                    continue 
                
                record = {}
                for i, cell in enumerate(cells):
                    key = headers[i] if i < len(headers) and headers[i] else f"{DEFAULT_COLUMN_PREFIX} {i+1}"
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
    for signatures, framework_name in FRAMEWORK_DETECTION_RULES:
        if any(sig in html_text for sig in signatures):
            return framework_name
    return DEFAULT_FRAMEWORK

