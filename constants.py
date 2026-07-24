import re

# HTML Parser & Default Tags
DEFAULT_HTML_PARSER = 'lxml'
DEFAULT_PAGE_TITLE = "No Title"
DEFAULT_SCHEME = "https://"
SUPPORTED_SCHEMES = ("http://", "https://")

# Structural & Grid Scraper Selectors
SECTION_TAGS = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer', 'table']
HEADING_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
IGNORED_GRID_TAGS = {'html', 'body', 'head', 'script', 'style', 'table', 'tbody', 'thead', 'tfoot', 'tr', 'td', 'th'}
FALLBACK_SEARCH_TARGETS = ['article', 'body']
TABLE_CELL_TAGS = ['td', 'th']
DEFAULT_COLUMN_PREFIX = "Column"

# Element Attribute Identifiers & Formatting
SCRAPER_ID_ATTR = "data-scraper-id"
SECTION_ID_PREFIX = "section-"

# Parsing & Truncation Bounds (Magic Numbers)
MAX_SECTION_PREVIEW_LEN = 150
MAX_TEXT_SNIPPET_LEN = 500
MIN_GRID_TEXT_LEN = 10
MAX_GRID_TEXT_LEN = 3000
MIN_SIGNATURE_DEPTH = 3
MIN_GRID_REPETITION_COUNT = 3

# Regular Expression Patterns
CURRENCY_REGEX = re.compile(r'[$₹€£]\s?\d+(?:\.\d{2})?')
EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_REGEX = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
CARD_CLASS_REGEX = re.compile(r'card|item|post|quote|product', re.IGNORECASE)

# Entity Extraction Metadata Keywords
METADATA_SEARCH_TAGS = ['p', 'span', 'div', 'i']
METADATA_KEYWORDS = ['rating', 'star', 'score', 'review']
METADATA_JOIN_DELIMITER = " | "

# Framework Detection Rules & Fallback String
FRAMEWORK_DETECTION_RULES = [
    (["id=\"root\"", "__NEXT_DATA__"], "Built with React"),
    (["id=\"app\"", "data-v-"], "Built with Vue"),
    (["ng-version"], "Built with Angular")
]
DEFAULT_FRAMEWORK = "Static or unknown framework"
