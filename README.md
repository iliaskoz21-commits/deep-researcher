# 🚀 DeepResearcher-ADK

> **Autonomous Research Microservice with Google Agent Development Kit (ADK), Gemini Flash & FastAPI.**

A production-ready AI microservice powered by the official **Google Agent Development Kit (ADK)** and **Gemini Flash**. The autonomous agent conducts deep web research, evaluates sources, scrapes relevant articles, and synthesizes comprehensive Markdown reports with citations.

---

## 🏛️ System Architecture

```
                        ┌─────────────────────────────────┐
                        │          FastAPI Server         │
                        │        POST /api/v1/research    │
                        └────────────────┬────────────────┘
                                         │
                        ┌────────────────▼────────────────┐
                        │    Google ADK Research Agent    │
                        │         (Gemini Flash)          │
                        └───────┬─────────────────┬───────┘
                                │                 │
                 ┌──────────────▼┐       ┌────────▼─────────────┐
                 │  search_web   │       │  fetch_web_content   │
                 │  (DuckDuckGo) │       │    (HTML Scraper)    │
                 └───────────────┘       └──────────────────────┘
```

### Key Features
- **Google ADK Native**: Built using Google's official `Agent`, `Runner`, and `InMemorySessionService` primitives.
- **Gemini Flash Engine**: High-speed reasoning, large context window, and minimal execution cost.
- **Zero-Cost Web Grounding**: Live search and scraping without requiring paid search API subscriptions.
- **Production REST API**: FastAPI backend with Pydantic validation, CORS support, and interactive Swagger documentation (`/docs`).

---

## 📁 Repository Structure

```
deep-researcher/
│
├── tools.py          # Python functions registered as Gemini Function Tools
├── agent.py          # Google ADK Agent configuration, Prompts & Runner workflow
├── main.py           # FastAPI REST API endpoints & schemas
├── requirements.txt  # Project dependencies
├── .env.example      # Environment variable template
└── README.md         # Project documentation
```

---

## ⚡ Quick Start & Installation

### 1. Prerequisites & Environment Setup
```bash
# Clone the repository
git clone https://github.com/iliaskoz21-commits/deep-researcher.git
cd deep-researcher

# Create a Python virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the template and supply your Gemini API key:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
*(Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/)).*

### 3. Run the Server
```bash
python main.py
```
The API server will start at `http://127.0.0.1:8000`.

---

## 📖 API Documentation & Testing

Once the server is running, explore the interactive Swagger documentation:
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
