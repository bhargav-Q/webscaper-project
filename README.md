# 🌐 Quantana — Enterprise Web Extraction System

A full-stack web scraping application that combines a **FastAPI** backend with a **React (Vite)** frontend to deliver a powerful two-step extraction workflow. Quantana leverages the [Bright Data Web Unlocker API](https://brightdata.com/) to fetch and render JavaScript-heavy pages, then uses **BeautifulSoup** to intelligently parse and extract structured data — all through a sleek, dark-themed dashboard.

> **Why Quantana?** Most scrapers blindly dump an entire page. Quantana lets you **preview** a website's structural sections first, **select** only the parts you care about, and then **extract** clean, structured data — saving time, bandwidth, and API credits.

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture Overview](#-architecture-overview)
- [Prerequisites and Dependencies](#-prerequisites-and-dependencies)
- [Installation and Setup](#-installation-and-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Backend Setup (Python)](#2-backend-setup-python)
  - [3. Frontend Setup (React)](#3-frontend-setup-react)
- [Usage](#-usage)
  - [Running the Application](#running-the-application)
  - [Two-Step Extraction Workflow](#two-step-extraction-workflow)
  - [API Endpoints](#api-endpoints)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License and Credits](#-license-and-credits)

---

## ✨ Features

- **Two-Step Extraction Flow** — Preview page sections before scraping, so you only extract what matters.
- **Bright Data Integration** — Fetches pages through the Bright Data Web Unlocker API with full JavaScript rendering support.
- **Smart Section Detection** — Automatically identifies semantic HTML5 sections (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`) with a fallback to structural `<div>` analysis.
- **Framework Detection** — Detects whether the target site is built with React, Vue, Angular, or is static HTML.
- **Structured Data Extraction** — Extracts headings, links, images, paragraphs, and email addresses into clean, tabulated data.
- **CSV Export** — One-click export of any extracted data category to CSV format.
- **HTML Caching** — Caches fetched HTML in-memory to avoid redundant API calls and save Bright Data credits.
- **Modern React Dashboard** — A glassmorphism-styled dark UI built with React 19, Vite 8, and Lucide icons.
- **RESTful API** — Clean FastAPI backend with CORS support, ready for integration with any frontend or automation tool.

---

## 🏗 Architecture Overview

```
┌─────────────────────────┐         ┌─────────────────────────┐
│     React Frontend      │  HTTP   │     FastAPI Backend      │
│    (Vite · Port 5173)   │◄───────►│     (Uvicorn · Port 8000)│
│                         │         │                         │
│  HeroSection            │         │  /api/health            │
│  PreviewCards            │         │  /api/preview           │
│  ResultsDashboard        │         │  /api/scrape            │
└─────────────────────────┘         └────────┬────────────────┘
                                             │
                                             │ HTTPS
                                             ▼
                                   ┌─────────────────────┐
                                   │  Bright Data API     │
                                   │  (Web Unlocker)      │
                                   └─────────────────────┘
```

---

## 📋 Prerequisites and Dependencies

Before setting up Quantana, ensure you have the following installed:

| Requirement | Version | Purpose |
|---|---|---|
| **Python** | 3.8+ | Backend runtime |
| **Node.js** | 18+ | Frontend build tooling |
| **npm** | 9+ | Package management for frontend |
| **Git** | Any | Cloning the repository |
| **Bright Data Account** | — | Required for the Web Unlocker API token |

### Key Backend Libraries

| Library | Purpose |
|---|---|
| `fastapi` | Web framework for the REST API |
| `uvicorn` | ASGI server to run FastAPI |
| `beautifulsoup4` + `lxml` | HTML parsing and data extraction |
| `requests` | HTTP client for Bright Data API calls |
| `python-dotenv` | Loads environment variables from `.env` |
| `pydantic` | Request/response data validation |

### Key Frontend Libraries

| Library | Purpose |
|---|---|
| `react` (v19) | UI component library |
| `vite` (v8) | Build tool and dev server |
| `lucide-react` | Icon library |

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/webscaper-project-learning.git
cd webscaper-project-learning
```

### 2. Backend Setup (Python)

Create and activate a virtual environment, then install dependencies:

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### Configure Environment Variables

1. **Backend**: Create a `.env` file in the project root (or copy from `.env.example`):

```env
# Backend Environment Variables
BRIGHTDATA_API_TOKEN=your_brightdata_api_token_here
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

> ⚠️ **Important:** Never commit your `.env` file. It is already included in `.gitignore`. A template file `.env.example` is committed for reference.

### 3. Frontend Setup (React)

```bash
cd frontend
npm install
```

#### Configure Frontend Environment Variables

Create a `.env` file inside the `frontend/` directory (or copy from `frontend/.env.example`):

```env
# Frontend Environment Variables (Vite)
VITE_API_BASE_URL=http://localhost:8000
```

---

## 💡 Usage

### Running the Application

You need **two terminal windows** — one for the backend and one for the frontend.

**Terminal 1 — Start the Backend:**

```bash
# From the project root
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Start the Frontend:**

```bash
# From the frontend/ directory
cd frontend
npm run dev
```

The frontend will be available at **http://localhost:5173** and the backend API at **http://localhost:8000**.

### Two-Step Extraction Workflow

1. **Enter a URL** — Type any website URL into the search bar on the hero screen and click **"Analyze URL"**.
2. **Preview Sections** — Quantana fetches the page via Bright Data, identifies structural sections, and displays them as selectable cards. Each card shows the HTML tag, class name, and a text preview.
3. **Select & Extract** — Check the sections you want to extract (or leave all unchecked to extract the full page), then click **"Extract"**.
4. **View Results** — Browse the extracted data (headings, links, images, paragraphs, emails) in a tabbed dashboard.
5. **Export to CSV** — Click the **"Export"** button to download the currently active tab's data as a CSV file.

### API Endpoints

| Method | Endpoint | Description | Request Body |
|---|---|---|---|
| `GET` | `/api/health` | Health check | — |
| `POST` | `/api/preview` | Fetch a page and return section previews | `{ "url": "https://example.com" }` |
| `POST` | `/api/scrape` | Extract data from selected sections | `{ "url": "https://example.com", "selected_sections": [...] }` |

**Example — Preview a website:**

```bash
curl -X POST http://localhost:8000/api/preview \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Example Response (Preview):**

```json
{
  "success": true,
  "url": "https://example.com",
  "title": "Example Domain",
  "framework": "Static or unknown framework",
  "sections": [
    {
      "section_id": "section-0",
      "tag": "header",
      "class": "",
      "id": "",
      "preview": "Example Domain This domain is for use in illustrative examples..."
    }
  ]
}
```

---

## 📁 Project Structure

```
webscaper-project-learning/
├── .env                    # Backend environment variables (not committed)
├── .env.example            # Backend environment template (committed)
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── main.py                 # FastAPI app — routes, dynamic CORS, caching
├── fetcher.py              # Bright Data API integration — page fetching
├── analyser.py             # HTML parsing — section scanning, data extraction
├── utils.py                # Utility functions (extensible)
│
└── frontend/               # React + Vite frontend
    ├── .env                # Frontend environment variables (not committed)
    ├── .env.example        # Frontend environment template (committed)
    ├── .gitignore          # Frontend git ignore rules
    ├── package.json        # Node.js dependencies and scripts
    ├── vite.config.js      # Vite configuration
    ├── index.html          # HTML entry point
    └── src/
        ├── main.jsx        # React entry point
        ├── App.jsx         # Main app — dynamic API_BASE_URL, state routing
        ├── App.css         # Application styles (glassmorphism dark theme)
        ├── index.css       # Global styles and CSS variables
        └── components/
            ├── HeroSection.jsx       # URL input and landing page
            ├── PreviewCards.jsx      # Section preview and selection UI
            └── ResultsDashboard.jsx  # Tabbed data display and CSV export
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** this repository
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and commit with descriptive messages:
   ```bash
   git commit -m "Add: description of your change"
   ```
4. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** with a clear description of what you changed and why.

### Guidelines

- Follow the existing code style and project structure.
- Test your changes with both the frontend and backend running.
- Update documentation if your change affects usage or setup.
- Keep pull requests focused — one feature or fix per PR.

### Reporting Issues

Found a bug or have a feature request? [Open an issue](https://github.com/<your-username>/webscaper-project-learning/issues) with:
- A clear title and description
- Steps to reproduce (for bugs)
- Expected vs. actual behavior

---

## 📜 License and Credits

### License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

### Credits & Acknowledgements

| Resource | Role |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Backend web framework |
| [React](https://react.dev/) | Frontend UI library |
| [Vite](https://vite.dev/) | Frontend build tool and dev server |
| [Bright Data](https://brightdata.com/) | Web Unlocker API for page fetching with JS rendering |
| [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) | HTML parsing and extraction |
| [lxml](https://lxml.de/) | High-performance HTML/XML parser |
| [Lucide React](https://lucide.dev/) | Icon set for the frontend UI |
| [Uvicorn](https://www.uvicorn.org/) | Lightning-fast ASGI server |

---

<p align="center">
  Built with ☕ and curiosity — <strong>Quantana</strong> © 2026
</p>
