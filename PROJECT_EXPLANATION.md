# 🌐 Quantana — Comprehensive System Explanation & Architecture Guide

Welcome to the technical handbook for the **Quantana Enterprise Web Extraction System**. This document provides an exhaustive, line-by-line, and component-by-component explanation of how this project is designed, how the frontend and backend talk to each other, the engineering fundamentals of web extraction, and the development patterns used.

---

## 📑 Table of Contents
1. [System Architecture & Data Flow](#1-system-architecture--data-flow)
2. [Backend Deep Dive (FastAPI & BeautifulSoup4)](#2-backend-deep-dive-fastapi--beautifulsoup4)
   - [main.py (The Orchestrator)](#mainpy-the-orchestrator)
   - [fetcher.py (The Network & Proxy Layer)](#fetcherpy-the-network--proxy-layer)
   - [analyser.py (The HTML Parsing Engine)](#analyserpy-the-html-parsing-engine)
   - [utils.py (DOM Analyzer & Regex Detectors)](#utilspy-dom-analyzer--regex-detectors)
3. [Frontend Deep Dive (React 19 & Vite 8)](#3-frontend-deep-dive-react-19--vite-8)
   - [App.jsx (State Machine & API Integration)](#appjsx-state-machine--api-integration)
   - [HeroSection.jsx (The Search Gateway)](#herosectionjsx-the-search-gateway)
   - [PreviewCards.jsx (Target Selection UI)](#previewcardsjsx-target-selection-ui)
   - [ResultsDashboard.jsx (Tabular Data & Exporter)](#resultsdashboardjsx-tabular-data--exporter)
4. [Software Engineering Fundamentals Used](#4-software-engineering-fundamentals-used)
   - [HTTP, REST & CORS](#http-rest--cors)
   - [Dynamic Rendering & Anti-Bot Bypass](#dynamic-rendering--anti-bot-bypass)
   - [In-Memory Caching Pattern](#in-memory-caching-pattern)
   - [DOM Signature Hashing (Pattern Matching)](#dom-signature-hashing-pattern-matching)
   - [Entity Detection via Regular Expressions (Regex)](#entity-detection-via-regular-expressions-regex)
5. [Development Principles for Production Systems](#5-development-principles-for-production-systems)

---

## 1. System Architecture & Data Flow

Quantana uses a decoupled **Client-Server Architecture** which communicates via RESTful JSON APIs.

```
┌─────────────────────────────────┐                 ┌─────────────────────────────────┐
│         React Frontend          │                 │         FastAPI Backend         │
│       (Vite · Port 5173)        │                 │      (Uvicorn · Port 8000)      │
│                                 │                 │                                 │
│  1. Submit URL ─────────────────┼─ POST /preview ─┼─► 1. Check Cache                │
│                                 │                 │   2. Fetch from Bright Data     │
│  2. Render Target Preview ◄─────┼── JSON Response ┼───3. Detect Framework & Stats   │
│     Cards (Select Sections)     │                 │   4. Cache Annotated HTML       │
│                                 │                 │                                 │
│  3. Submit Selected Sections ───┼─ POST /scrape ──┼─► 1. Read Cache / Re-Fetch      │
│                                 │                 │   2. Extract Entities/Tables    │
│  4. Render Tabulated Results ◄──┼── JSON Response ┼───3. Respond with clean JSON     │
│     & Download CSV / JSON       │                 │                                 │
└─────────────────────────────────┘                 └─────────────────────────────────┘
```

---

## 2. Backend Deep Dive (FastAPI & BeautifulSoup4)

The backend is built in Python using **FastAPI** for high performance and **BeautifulSoup4** (with `lxml` parser) for lightning-fast parsing of the HTML Document Object Model (DOM).

### `main.py` (The Orchestrator)
This file defines the FastAPI application instance, sets up communication permissions, and exposes the HTTP endpoints.

*   **FastAPI Initialization (Lines 8-9):**
    ```python
    app = FastAPI(title="Web Scraper API", version="2.0.0")
    ```
    FastAPI uses automatic documentation generation. Navigating to `http://localhost:8000/docs` displays a Swagger UI interactively showing all endpoints.
*   **CORS Configuration (Lines 11-18):**
    ```python
    allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```
    Browsers enforce the **Same-Origin Policy** which blocks scripts on one origin (port 5173) from requesting resources from another (port 8000). Quantana dynamically reads allowed origins from the `ALLOWED_ORIGINS` environment variable, defaulting to local dev ports (`5173` and `3000`). CORS middleware adds headers (`Access-Control-Allow-Origin`) to allow React to communicate with FastAPI.
*   **HTML Cache (Line 22):**
    ```python
    html_cache = {}
    ```
    An in-memory Python dictionary mapping target URLs to their fetched HTML string (which contains injected tracking IDs). This prevents charging the user multiple API credits for fetching the same page during a single session.
*   **Endpoints:**
    1.  `/api/health` [GET]: Simple health monitor to verify the backend is responsive.
    2.  `/api/preview` [POST]: Accepts a URL inside a `PreviewRequest` Pydantic model. Normalizes the URL (prepends `https://` if missing), fetches the HTML page, scans it for structural sections, caches the annotated HTML, calculates DOM statistics (like link/image count), and returns section metadata to the UI.
    3.  `/api/scrape` [POST]: Accepts a URL and an array of `selected_sections`. Reads HTML from the cache (or fetches it if missing), extracts tabular/relational record arrays, and outputs the final JSON payload.

---

### `fetcher.py` (The Network & Proxy Layer)
This file interfaces with external servers to download page HTML.

*   **API Configuration (Lines 14-32):**
    ```python
    def fetch_page(url):
        brightdata_token = os.getenv("BRIGHTDATA_API_TOKEN")
        api_url = "https://api.brightdata.com/request"
        headers = { ... }
        payload = {
            "zone": "web_unlocker1",
            "url": url,
            "format": "raw"
        }
    ```
    Rather than making a simple `requests.get(url)` which would get instantly blocked by security engines like Cloudflare or Akamai on modern enterprise websites, Quantana uses the **Bright Data Web Unlocker API**. 
    - It routes requests through residential/datacenter proxy IPs.
    - It automatically solves CAPTCHAs, manages cookies, and spoofs browser headers.
    - It uses headless browsers under the hood to fully execute Javascript arrays (e.g., dynamic React routes) before returning the finalized static DOM.
*   **UTF-8 Encoding Force (Line 42):**
    ```python
    response.encoding = 'utf-8'
    ```
    Forces the response decoding to UTF-8 to prevent string decoding bugs (such as corrupted symbols like `£`, `€`, or emoji codes).

---

### `analyser.py` (The HTML Parsing Engine)
This file contains the logic that scans, tags, and extracts data from HTML files.

*   **Semantic Section Tagging (Lines 15-42):**
    The scraper searches for structural elements (`header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `table`). 
    It iterates through these tags:
    1.  Extracts a brief string preview of the text inside the section: `tag.get_text(separator=' ', strip=True)[:150]`.
    2.  Injects a tracking attribute directly into the BeautifulSoup element node tree: `tag['data-scraper-id'] = section_id`.
    3.  Appends this metadata (ID, Tag name, CSS classes, HTML ID, and Text Preview) to a list.
*   **Grid Hashing Integration (Lines 43-62):**
    If a page does not use semantic elements, `scan_sections` invokes `DOMAnalyzer` to seek repeating grids and appends them to the preview array. It then returns the list of cards along with the stringified version of the annotated HTML (which now has `data-scraper-id="..."` attached to target nodes).
*   **Locating Selected Targets (Lines 67-75):**
    ```python
    def _find_section_element(soup, section_info):
        section_id = section_info.get("section_id")
        if section_id:
            return soup.find(attrs={"data-scraper-id": section_id})
    ```
    During the scrape step, when the frontend sends back the checked section cards, this helper uses the unique tracking IDs to target specific DOM nodes inside BeautifulSoup instantly.
*   **Universal Scraper Algorithm (Lines 78-140):**
    For each target element being scraped:
    - **Tabular Data Extractor:** If the element is a `<table>`, it locates all column headers `<th>`, iterates over every table row `<tr>`, processes each cell `<td>`, and compiles them into clean key-value relational maps (e.g. `{"Column 1": "value", "Column 2": "value"}`).
    - **Record Extractor:** For non-table tags, it passes the elements into the `EntityDetector` class which uses structure and heuristics to capture semantic patterns.
*   **Framework Detection (Lines 143-154):**
    Looks for telltale fingerprints of popular client-side framework templates:
    - `id="root"` or `__NEXT_DATA__` (Next.js/React standard root wrappers)
    - `id="app"` or `data-v-` (Vue.js template properties)
    - `ng-version` (Angular standard metadata properties)

---

### `utils.py` (DOM Analyzer & Regex Detectors)
This file provides specialized helper classes that automate visual block detection and field classifications.

*   **DOM Grid Hashing Pattern (`DOMAnalyzer`):**
    Traditional scrapers fail when class names change dynamically (e.g. TailwindCSS hash classes like `class="css-1a2b3c"`). Quantana solves this using structural fingerprinting:
    ```python
    def _get_signature(self, element):
        tags = [element.name]
        for child in element.find_all(recursive=False):
            if child.name:
                tags.append(child.name)
        return "-".join(tags)
    ```
    1.  For any HTML element, `_get_signature` creates a string representing its direct child nodes (e.g., a card container containing a title, text, and an image would return a signature of `div-h3-p-img`).
    2.  `find_grids()` loops through the DOM, calculating signatures.
    3.  If a signature is encountered 3 or more times (`if count >= 3:`), it flags those elements as repeating dynamic templates (like eCommerce listings, news grids, or testimonials).
*   **Regex-based Data Extractors (`EntityDetector`):**
    Uses compiled Regular Expressions (Regex) to extract structured entity records from unstructured text:
    - **Price:** `[$₹€£]\s?\d+(?:\.\d{2})?` (Matches currency symbols followed by decimals)
    - **Email:** `[\w\.-]+@[\w\.-]+\.\w+` (Captures common email patterns)
    - **Phone:** `\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}` (Matches US/generic formatted phone numbers)
    - **Titles, Images, and Links:** Uses BeautifulSoup structures to extract image `src` targets, header values, anchor URLs, and ratings/stars (based on CSS class search terms containing "star", "rating", "score").

---

## 3. Frontend Deep Dive (React 19 & Vite 8)

The frontend is a lightweight Single Page Application (SPA). It uses **Vite** for super-fast Hot Module Replacement (HMR) during coding and compiled asset bundles for deployment.

### `App.jsx` (State Machine & API Integration)
This file maintains state management, handles async fetching, and coordinates UI views.

*   **Environment-Driven API Configuration (Line 7):**
    ```javascript
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
    ```
    Loads the backend endpoint dynamically from `.env` using Vite's `import.meta.env`, preventing hardcoded backend URLs in production deployments.
*   **View-Based State Machine (Lines 9-15):**
    ```javascript
    const [appState, setAppState] = useState('HERO'); // HERO, PREVIEW, RESULTS
    ```
    Instead of maintaining messy boolean flags (like `isHeroVisible = true`), `appState` acts as a state router. The UI updates dynamically to present:
    - `HeroSection` (if `HERO`)
    - `PreviewCards` (if `PREVIEW`)
    - `ResultsDashboard` (if `RESULTS`)
*   **HTTP Async Operations:**
    Using ES6 `fetch` with `async` / `await` to make POST requests to `${API_BASE_URL}/api/preview` and `${API_BASE_URL}/api/scrape`. It monitors `loading` hooks to disable buttons and trigger animated progress indicators.

---

### `HeroSection.jsx` (The Search Gateway)
The entry landing screen.

*   Exposes a form input with standard HTML input validation hooks.
*   Triggers the `onAnalyze(url)` parent state callback upon submission.
*   Leverages `lucide-react` icons to create a beautiful, modern look.

---

### `PreviewCards.jsx` (Target Selection UI)
This screen allows developers/users to interactively filter and select which elements of the target DOM should be extracted.

*   **Interactive Target Searching (Lines 8-14):**
    Enables instant filtering of sections as the user types, matches by HTML tag name, CSS class names, or string previews.
*   **DOM Stats Counter (Lines 43-52):**
    Shows a breakdown of the DOM nodes extracted (Articles count, Cards count, Images count, etc.) to give the user a clear picture of the page complexity before running full scrapes.
*   **Checkbox Selection Management:**
    Users can check specific sections or press "Select All" to target everything. The floating bottom button updates dynamically showing how many blocks are queued for parsing.

---

### `ResultsDashboard.jsx` (Tabular Data & Exporter)
Once extraction completes, the data is rendered in a modern grid structure.

*   **Dynamic Column Detection (Lines 8-18):**
    Since different websites contain different fields (some have price & email, others have image & description), the columns are computed dynamically by collecting all unique keys from all records using a JavaScript `Set`:
    ```javascript
    const allKeysSet = new Set();
    records.forEach(r => Object.keys(r).forEach(k => allKeysSet.add(k)));
    ```
    It then sorts these columns using a `standardOrder` template to make sure crucial fields like `Title` and `Price` always appear on the far left.
*   **CSV Downloader (Lines 20-42):**
    1.  Loop through headers and row entries.
    2.  Clean value strings by replacing quotes with double-quotes to preserve valid CSV structures: `replace(/"/g, '""')`.
    3.  Creates a virtual URL data link containing the URI-encoded CSV content: `encodeURI("data:text/csv;charset=utf-8,...")`.
    4.  Appends a mock `<a>` element to the DOM, triggers programmatically `.click()`, and instantly cleans up.

---

## 4. Software Engineering Fundamentals Used

Building high-performance, robust software requires applying fundamental design patterns:

### HTTP, REST & CORS
*   **HTTP Methods:** Uses `GET` for fetching status and `POST` for sending data payloads. POST requests are essential here since we are sending JSON bodies with target URLs and selection configurations.
*   **CORS (Cross-Origin Resource Sharing):** Security configuration built into web browsers to control API requests between different domains. Configuring CORS allows our frontend domain (`localhost:5173`) access to API data from the backend server (`localhost:8000`).

### Dynamic Rendering & Anti-Bot Bypass
*   Modern frontends (like React) construct websites in real-time in the browser. Traditional scrapers (like basic Python `requests`) only fetch raw HTML, resulting in empty layouts. Quantana uses **Bright Data Web Unlocker** to execute JavaScript, render the virtual DOM, bypass anti-scraping systems, and return a clean, fully-rendered DOM.

### In-Memory Caching Pattern
*   Whenever a preview is generated, the annotated HTML is saved in a memory structure (`html_cache`). When the subsequent "Scrape" request fires, it reads directly from RAM. This represents a significant optimization:
    - **Time Savings:** Skips a network request that can take 15-30 seconds.
    - **Cost Savings:** Bright Data charge per successful request; caching saves API credits.

### DOM Signature Hashing (Pattern Matching)
*   Instead of hardcoding CSS classes (which break when websites update their designs), Quantana maps the relative structure of child trees. Generating tag signatures like `div-span-a-img` allows it to identify dynamic card lists without knowing the class name conventions beforehand.

### Entity Detection via Regular Expressions (Regex)
*   Regex is a powerful pattern matching syntax used to find occurrences of string structures. The `EntityDetector` uses regex to reliably scan paragraphs for currency patterns (`$100`, `£45.50`), email formats (`contact@domain.com`), and telephone formats.

---

## 5. Development Principles for Production Systems

Quantana follows core development rules that make software reliable and maintainable:

1.  **Defensive Validation:** Pydantic models validate data shapes at the API entry point, returning clean `422 Unprocessable Entity` responses if request schemas are wrong.
2.  **Graceful Degradation:** The scraping functions fallback to the full page body if custom grids or semantic tags cannot be located. The system prioritizes delivering *some* data over throwing exceptions.
3.  **UI Feedback and State Protection:** Buttons are disabled and loading indicators are displayed while network processes are pending. This keeps users informed and prevents double-clicks from spawning duplicate network operations.
4.  **No Mock Data:** The backend does not use dummy mock lists. It processes and transforms real DOM tags fetched from real web addresses.
