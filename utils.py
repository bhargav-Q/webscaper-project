import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from constants import (
    CARD_CLASS_REGEX,
    CURRENCY_REGEX,
    EMAIL_REGEX,
    HEADING_TAGS,
    IGNORED_GRID_TAGS,
    MAX_GRID_TEXT_LEN,
    MAX_TEXT_SNIPPET_LEN,
    METADATA_JOIN_DELIMITER,
    METADATA_KEYWORDS,
    METADATA_SEARCH_TAGS,
    MIN_GRID_REPETITION_COUNT,
    MIN_GRID_TEXT_LEN,
    MIN_SIGNATURE_DEPTH,
    PHONE_REGEX,
)

class EntityDetector:
    def __init__(self, base_url=""):
        self.base_url = base_url

    def extract_entities(self, element):
        text_content = element.get_text(separator=' ', strip=True)
        entities = {}
        
        # 1. Price
        price_match = CURRENCY_REGEX.search(text_content)
        if price_match:
            entities['Price'] = price_match.group(0)

        # 2. Email
        email_match = EMAIL_REGEX.search(text_content)
        if email_match:
            entities['Email'] = email_match.group(0)

        # 3. Phone (Basic)
        phone_match = PHONE_REGEX.search(text_content)
        if phone_match:
            entities['Phone'] = phone_match.group(0)

        # 4. Title
        heading = element.find(HEADING_TAGS)
        if heading:
            a_tag = heading.find('a')
            if a_tag and a_tag.get('title'):
                entities['Title'] = a_tag.get('title').strip()
            else:
                entities['Title'] = heading.get_text(strip=True)
        else:
            # Fallback for title: first bold or strong or prominent link
            a_tag = element.find('a')
            if a_tag:
                entities['Title'] = a_tag.get_text(strip=True)
            
        # 5. Image & Link
        img = element.find('img')
        raw_img = img.get('src', '') if img else ""
        if raw_img:
            entities['Image'] = urljoin(self.base_url, raw_img)
            
        link = element.find('a', href=True)
        raw_link = link.get('href', '') if link else ""
        if raw_link:
            entities['Link'] = urljoin(self.base_url, raw_link)
            
        # 6. Metadata/Ratings
        metadata_list = []
        for tag in element.find_all(METADATA_SEARCH_TAGS):
            class_str = " ".join(tag.get('class', [])).lower()
            if any(keyword in class_str for keyword in METADATA_KEYWORDS):
                metadata_list.append(class_str.replace('-', ' ').title())
        if metadata_list:
            # use set to remove duplicates
            entities['Metadata'] = METADATA_JOIN_DELIMITER.join(list(set(metadata_list)))

        # 7. Text block
        paragraphs = [p.get_text(strip=True) for p in element.find_all('p')]
        if paragraphs:
            entities['Text'] = METADATA_JOIN_DELIMITER.join(p for p in paragraphs if p)
        else:
            if heading:
                heading.extract()
            rem_text = element.get_text(separator=' ', strip=True)
            entities['Text'] = rem_text[:MAX_TEXT_SNIPPET_LEN] + "..." if len(rem_text) > MAX_TEXT_SNIPPET_LEN else rem_text

        return {k: v for k, v in entities.items() if v}


class DOMAnalyzer:
    def __init__(self, soup):
        self.soup = soup
        self.signature_counts = {}
        self.element_map = {}
        
    def get_stats(self):
        return {
            "articles": len(self.soup.find_all('article')),
            "images": len(self.soup.find_all('img')),
            "links": len(self.soup.find_all('a')),
            "cards": len(self.soup.find_all(class_=CARD_CLASS_REGEX)),
            "forms": len(self.soup.find_all('form')),
            "tables": len(self.soup.find_all('table'))
        }
        
    def _get_signature(self, element):
        tags = [element.name]
        for child in element.find_all(recursive=False):
            if child.name:
                tags.append(child.name)
        return "-".join(tags)

    def find_grids(self):
        """ Returns all nodes that are part of a repeated structural grid. """
        for tag in self.soup.find_all(True):
            # Skip structural wrappers, scripts, and table elements (handled explicitly)
            if tag.name in IGNORED_GRID_TAGS:
                continue
                
            text = tag.get_text(strip=True)
            if len(text) < MIN_GRID_TEXT_LEN or len(text) > MAX_GRID_TEXT_LEN:
                continue
                
            sig = self._get_signature(tag)
            if len(sig.split('-')) < MIN_SIGNATURE_DEPTH:
                continue
                
            if sig not in self.signature_counts:
                self.signature_counts[sig] = 0
                self.element_map[sig] = []
                
            self.signature_counts[sig] += 1
            self.element_map[sig].append(tag)
            
        grids = []
        for sig, count in self.signature_counts.items():
            if count >= MIN_GRID_REPETITION_COUNT:
                grids.extend(self.element_map[sig])
        return grids

