# Web Scraper Project

A full-stack web application for structural preview and selective web scraping. It uses FastAPI and BeautifulSoup on the backend to parse dynamic web pages fetched via the Bright Data Web Unlocker API, and React (Vite) on the frontend for visual section selection and structured data display.

## What It Does

The application splits web scraping into a two-step flow:
1. **Target Identification (Preview)**: Fetches dynamic HTML, parses structural elements and repeated DOM signatures into discrete section cards, and computes page DOM statistics.
2. **Selective Extraction (Scrape)**: Isolates user-selected sections and applies heuristic entity detectors (prices, emails, phone numbers, links, titles, metadata) or tabular parsers to extract relational records.

---

## Setup & Local Execution

### Prerequisites
* Python 3.10+
* Node.js 18+ and npm

### 1. Backend Setup

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.example .env
```

Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```
Backend runs at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Create frontend .env from template
cp .env.example .env
```

Start the Vite development server:
```bash
npm run dev
```
Frontend runs at `http://localhost:5173`.

---

## Environment Variables

All environment variables must be defined in `.env` files (see `.env.example` in root and `/frontend`). Never commit real credential values.

| Variable Name | Location | Description |
| :--- | :--- | :--- |
| `BRIGHTDATA_API_TOKEN` | Backend `.env` | API token for Bright Data Web Unlocker authentication. |
| `BRIGHTDATA_API_URL` | Backend `.env` | Endpoint URL for Bright Data request proxy (default: `https://api.brightdata.com/request`). |
| `BRIGHTDATA_ZONE` | Backend `.env` | Zone name configured in Bright Data dashboard (default: `web_unlocker1`). |
| `BRIGHTDATA_REQUEST_TIMEOUT` | Backend `.env` | Request timeout in seconds for web fetching operations (default: `180`). |
| `ALLOWED_ORIGINS` | Backend `.env` | Comma-separated list of allowed CORS origins for FastAPI middleware. |
| `VITE_API_BASE_URL` | Frontend `.env` | Base URL of the backend FastAPI service (default: `http://localhost:8000`). |

---

## Running Tests & Linters

* **Backend Tests**: Run `pytest` (when test files in `tests/` are present).
* **Frontend Linter**: Run `npm run lint` inside `/frontend` to execute `oxlint`.

---

## Project Structure

```
webscaper-project-learning/
├── main.py              # FastAPI application, CORS, endpoints & in-memory cache
├── analyser.py          # Section scanning (semantic/grid) & relational HTML extraction
├── fetcher.py           # Bright Data API request wrapper
├── utils.py             # DOM signature hashing (DOMAnalyzer) & entity regex detectors
├── config.py            # Environment configuration loader
├── constants.py         # Parsing rules, regex patterns, and default parameters
├── requirements.txt     # Backend Python dependencies
├── .env.example         # Template for backend environment variables
└── frontend/            # React (Vite) frontend
    ├── src/
    │   ├── App.jsx      # Core workflow state & screen manager
    │   ├── api/         # Axios/Fetch API service abstraction (scraperService.js)
    │   ├── components/  # HeroSection, PreviewCards, ResultsDashboard UI components
    │   └── constants/   # UI strings, data rules, app configurations
    └── package.json     # Frontend dependencies & scripts
```

---

## Architecture & Data Flow

```
[ User UI (React) ] ──(1) POST /api/preview ──> [ FastAPI (main.py) ]
                                                        │
                                                        ▼
                                                [ Bright Data API ]
                                                        │
                                                        ▼ (Raw Rendered HTML)
                                                [ scan_sections ]
                                                        │
  [ React State ] <── (2) Preview Cards & Stats ────────┤ (Injects data-scraper-id)
         │                                              │
         │                                              ▼
         └──────────(3) POST /api/scrape ────────> [ html_cache[url] ]
                        (Selected Sections)             │
                                                        ▼
                                                [ analyse_html ]
                                                        │
  [ User UI ] <──── (4) Relational JSON Data ───────────┘ (Entity & Table Parsing)
```

1. **Preview Phase**: Client posts target URL to `/api/preview`. Backend fetches dynamic HTML via Bright Data, scans for semantic tags (`<header>`, `<main>`, `<section>`) and structural grid repeats using `DOMAnalyzer`, injects synthetic `data-scraper-id` attributes, stores annotated HTML in `html_cache[url]`, and returns section cards with DOM stats.
2. **Scrape Phase**: Client selects section IDs and posts to `/api/scrape`. Backend looks up `html_cache[url]`, isolates selected section sub-trees using `data-scraper-id`, extracts tabular structures or regular expression entities (`EntityDetector`), and returns formatted JSON records.

---

## Gotchas & Engineering Decisions Log

1. **Synthetic ID Injection (`data-scraper-id`)**:
   * *Problem*: Scraped pages often lack standard `id` or `class` attributes on structural containers, making section targeting unreliable.
   * *Decision*: During the preview phase, `scan_sections()` mutates the in-memory BeautifulSoup tree to inject synthetic `data-scraper-id="sec_0"`, `sec_1` attributes into target nodes before stringifying and caching the HTML.

2. **In-Memory Credit Saving Cache (`html_cache`)**:
   * *Problem*: Fetching pages through Bright Data consumes API credits per request. Repeating requests for preview and scrape would double API costs.
   * *Decision*: Raw annotated HTML is cached in a global dictionary keyed by URL during preview. `/api/scrape` reuses the cached tree.
   * *Known Trade-off / Landmine*: `html_cache` is an un-bounded in-memory Python dictionary without TTL/eviction. If the backend process restarts between Preview and Scrape steps, `/api/scrape` falls back to a fresh fetch without annotated IDs, returning empty section matches.
