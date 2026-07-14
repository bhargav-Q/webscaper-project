import re
from bs4 import BeautifulSoup


# The structural tags that define major "sections" of a webpage
SECTION_TAGS = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']


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

    # 2. If we found very few semantic tags, fall back to structural divs
    if len(sections) < 3:
        body = soup.find('body')
        if body:
            # Unwrap single-child wrappers (like <div id="root"> or <div id="__next">)
            container = body
            while True:
                child_divs = container.find_all('div', recursive=False)
                if len(child_divs) == 1:
                    container = child_divs[0]
                else:
                    break
            
            # Now scan the children of the true layout container
            for div in container.find_all('div', recursive=False):
                div_id = div.get('id', '')
                div_class = ' '.join(div.get('class', []))
                preview_text = div.get_text(separator=' ', strip=True)[:150]

                # Skip empty or tiny divs
                if not preview_text or len(preview_text) < 20:
                    continue

                section_id = f"section-{section_index}"
                div['data-scraper-id'] = section_id
                
                sections.append({
                    "section_id": section_id,
                    "tag": "div",
                    "class": div_class,
                    "id": div_id,
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


def analyse_html(html_text, selected_sections=None):
    """
    Step 2 of the Two-Step Flow.
    Extracts data from the HTML. If selected_sections is provided,
    only extracts from those specific sections. Otherwise, extracts from the full page.
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
        # No sections selected — search the entire page
        search_targets = [soup]

    # Extract data from the target elements
    headings = []
    links = []
    images = []
    paragraphs = []

    for target in search_targets:
        # Headings
        for tag in target.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = tag.get_text(strip=True)
            if text:
                headings.append({"level": tag.name, "text": text})

        # Links
        for a_tag in target.find_all('a', href=True):
            text = a_tag.get_text(strip=True)
            href = a_tag['href']
            if href and not href.startswith('#'):
                links.append({"text": text or "(no text)", "url": href})

        # Images
        for img_tag in target.find_all('img'):
            src = img_tag.get('src', '')
            alt = img_tag.get('alt', '')
            if src:
                images.append({"src": src, "alt": alt})

        # Paragraphs
        for p_tag in target.find_all('p'):
            text = p_tag.get_text(strip=True)
            if text:
                paragraphs.append(text)

    # Emails (always search full page since they can be anywhere)
    emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html_text)))

    report = {
        "title": title,
        "summary": {
            "headings": len(headings),
            "links": len(links),
            "images": len(images),
            "paragraphs": len(paragraphs),
            "emails": len(emails),
        },
        "data": {
            "headings": headings,
            "links": links,
            "images": images,
            "paragraphs": paragraphs,
            "emails": emails
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
