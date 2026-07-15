from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from fetcher import fetch_page
from analyser import analyse_html, detect_dynamic_content, scan_sections, get_dom_stats

# Create the FastAPI application
app = FastAPI(title="Web Scraper API", version="2.0.0")

# CORS Middleware: Allows React frontend (port 5173) to talk to this backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- HTML CACHE ----------
# Stores the fetched HTML so we don't call Bright Data twice (saves credits!)
# Key: URL, Value: raw HTML string
html_cache = {}

# ---------- REQUEST MODELS ----------

class PreviewRequest(BaseModel):
    url: str

class ScrapeRequest(BaseModel):
    url: str
    selected_sections: Optional[list] = None  # If None, scrape the full page

# ---------- ENDPOINTS ----------

# Health check
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Web Scraper API is running!"}


# Step 1: Preview — Fetch page and return section previews
@app.post("/api/preview")
def preview_website(request: PreviewRequest):
    url = request.url

    # Ensure the URL has a protocol
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Fetch the page using Bright Data (with JS rendering)
    response = fetch_page(url)

    if not response or response.status_code != 200:
        status_code = response.status_code if response else "Network Error"
        return {
            "success": False,
            "error": f"Failed to fetch page. Status code: {status_code}"
        }

    # Scan for sections and cache the annotated HTML so selected section IDs remain available
    sections, annotated_html = scan_sections(response.text)
    html_cache[url] = annotated_html

    # Detect the framework
    framework = detect_dynamic_content(response.text)

    # Get the page title
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.title.text.strip() if soup.title else "No Title"
    
    # Get DOM stats
    dom_stats = get_dom_stats(response.text)

    return {
        "success": True,
        "url": url,
        "title": title,
        "framework": framework,
        "sections": sections,
        "dom_stats": dom_stats
    }


# Step 2: Scrape — Extract data from selected sections only
@app.post("/api/scrape")
def scrape_website(request: ScrapeRequest):
    url = request.url

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Try to use cached HTML first (saves Bright Data credits!)
    if url in html_cache:
        html_text = html_cache[url]
    else:
        # If not cached, fetch fresh
        response = fetch_page(url)
        if not response or response.status_code != 200:
            status_code = response.status_code if response else "Network Error"
            return {
                "success": False,
                "error": f"Failed to fetch page. Status code: {status_code}"
            }
        html_text = response.text

    # Extract data from selected sections (or full page if none selected)
    report = analyse_html(url, html_text, request.selected_sections)

    # Detect framework
    framework = detect_dynamic_content(html_text)

    return {
        "success": True,
        "url": url,
        "framework": framework,
        "report": report
    }