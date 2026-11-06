# 🚀 DeepResearcher-ADK

> **Autonomous Research Microservice with Google Agent Development Kit (ADK), Gemini Flash, FastAPI & Interactive Web UI.**

A production-ready AI microservice powered by the official **Google Agent Development Kit (ADK)** and **Gemini Flash**. The autonomous agent conducts deep web research, evaluates sources, scrapes relevant articles, and synthesizes comprehensive Markdown reports with citations.

Includes an interactive **Web Dashboard UI**, a full **Automated Testing Suite (`pytest`)**, and **Docker containerization**.

---

## 🏛️ System Architecture

```
                 ┌──────────────────────────────────────────────────┐
                 │          FastAPI Web Service (Port 8000)         │
                 │   GET / (Dashboard UI)  |  POST /api/v1/research │
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
- **Interactive Web Dashboard**: Beautiful Tailwind CSS UI served directly at root `/` with live research triggers, markdown preview, and copy-to-clipboard functionality.
- **Google ADK Native**: Built using Google's official `Agent`, `Runner`, and `InMemorySessionService` primitives.
- **Gemini Flash Engine**: High-speed reasoning, large context window, and minimal execution cost.
- **Zero-Cost Web Grounding**: Live search and scraping without requiring paid search API subscriptions.
- **Automated Test Suite**: Comprehensive unit and integration tests using `pytest` and `fastapi.testclient`.
- **Production Containerization**: Ready-to-deploy `Dockerfile` and `docker-compose.yml`.

---

## 📁 Repository Structure

```
deep-researcher/
│
├── static/
│   └── index.html        # Interactive Web Dashboard UI (Tailwind + Marked.js)
├── tests/
│   ├── test_tools.py     # Unit tests for web search and content scraper
│   └── test_api.py       # Integration tests for FastAPI endpoints
├── tools.py              # Python functions registered as Gemini Function Tools
├── agent.py              # Google ADK Agent configuration, Prompts & Runner workflow
├── main.py               # FastAPI REST API & static file server
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

#### 3. Run the Server
```bash
python main.py
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser to access the Web Dashboard.

---

### Option B: Run with Docker / Docker Compose

You can build and spin up the complete containerized service in one command:

```bash
docker compose up --build
```
The application will be live at `http://localhost:8000`.

---

## 🧪 Automated Testing

Run the automated test suite with `pytest`:

```bash
pytest -v
```

All 6 unit and integration test suites validate:
- Tool structure and query handling
- HTML tag stripping and content cleaning
- Health check and Web Dashboard routes
- Request payload validation and error handling

---

## 📖 API Documentation & Testing (Swagger)

FastAPI automatically generates interactive Swagger documentation:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### Example Request (cURL)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/research" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Latest advancements in Agentic AI and Function Calling 2026"}'
```

---

## 📄 License
This project is licensed under the Apache 2.0 License.
