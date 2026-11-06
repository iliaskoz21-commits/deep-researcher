# 🚀 DeepResearcher-ADK

> **Autonomous Research Agent with Google Agent Development Kit (ADK), Gemini Flash & Flask Web Interface.**

A clean, Pythonic AI microservice powered by the official **Google Agent Development Kit (ADK)** and **Gemini Flash**. The autonomous agent conducts deep web research, evaluates sources, scrapes relevant articles, and synthesizes comprehensive Markdown reports with citations.

The user interface is built with **Flask** and **Jinja2 templates** — keeping the entire stack 100% Pythonic, without complex JavaScript frameworks.

---

## 🏛️ System Architecture

```
                 ┌──────────────────────────────────────────────────┐
                 │          Flask Web Application (Port 5000)       │
                 │    GET, POST / (Jinja2) | POST /api/v1/research  │
                 └─────────────────────────┬────────────────────────┘
                                           │
                         ┌─────────────────▼───────────────┐
                         │    Google ADK Research Agent    │
                         │         (Gemini Flash)          │
                         └───────┬─────────────────┬───────┘
                                 │                 │
                  ┌──────────────▼┐       ┌────────▼─────────────┐
                  │  search_web   │       │  fetch_web_content   │
                  │  (DuckDuckGo) │       │    (HTML Scraper)    │
                  └───────────────┘       └──────────────────────┘
```

### Key Highlights
- **100% Pythonic Web UI**: Built with **Flask** and **Jinja2** templates (`templates/index.html`). No Node.js or JavaScript complexity.
- **Server-Side Markdown Rendering**: Converts agent reports to clean HTML using Python's `markdown` library.
- **Google ADK Native**: Powered by Google's official `Agent`, `Runner`, and `InMemorySessionService`.
- **Gemini Flash Engine**: High-speed reasoning, large context window, and minimal execution cost.
- **Zero-Cost Web Grounding**: Live web search and scraping without requiring paid search API subscriptions.
- **Automated Test Suite**: Unit and integration tests using `pytest` and Flask test client (`app.test_client()`).
- **Production Containerization**: Ready-to-deploy `Dockerfile` and `docker-compose.yml`.

---

## 📁 Repository Structure

```
deep-researcher/
│
├── templates/
│   └── index.html        # Flask Jinja2 Web Template (Forms & Results)
├── tests/
│   ├── test_tools.py     # Unit tests for web search and content scraper
│   └── test_api.py       # Integration tests for Flask routes
├── tools.py              # Python functions registered as Gemini Function Tools
├── agent.py              # Google ADK Agent configuration, Prompts & Runner workflow
├── main.py               # Flask Web Application & REST API
├── requirements.txt      # Project dependencies
├── Dockerfile            # Container image specification (Python 3.12-slim)
├── docker-compose.yml    # One-command container orchestration
├── .dockerignore         # Docker build exclusion rules
├── .gitignore            # Git exclusion rules
├── .env.example          # Environment variable template
└── README.md             # Project documentation
```

---

## ⚡ Quick Start & Installation

### Option A: Local Python Environment

#### 1. Setup Environment
```bash
# Clone the repository
git clone https://github.com/iliaskoz21-commits/deep-researcher.git
cd deep-researcher

# Create and activate a Python virtual environment
python -m venv .venv

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Environment Variables
```bash
cp .env.example .env
```
Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
*(Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/)).*

#### 3. Run the Flask Server
```bash
python main.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser to access the Flask web interface.

---

### Option B: Run with Docker / Docker Compose

You can build and spin up the complete containerized service in one command:

```bash
docker compose up --build
```
The application will be live at `http://localhost:5000`.

---

## 🧪 Automated Testing

Run the automated test suite with `pytest`:

```bash
pytest -v
```

All 6 unit and integration test suites validate:
- Tool structure and live query handling
- HTML tag stripping and content cleaning
- Health check route (`/api/health`)
- Flask web form rendering and template output
- JSON API endpoint (`/api/v1/research`)

---

## 📄 License
This project is licensed under the Apache 2.0 License.
