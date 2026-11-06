"""
main.py - FastAPI Backend Service for the Autonomous Research Agent.

Exposes REST API endpoints and serves an interactive web dashboard
allowing users or external services to trigger autonomous research workflows.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn
import uuid
import os

# Import the core agent execution workflow
from agent import execute_research

# Initialize FastAPI application
app = FastAPI(
    title="DeepResearcher ADK API",
    description="Production-ready REST API & Web UI powered by Google ADK and Gemini Flash for autonomous web research.",
    version="1.1.0"
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory if it exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Pydantic schema for request body
class ResearchRequest(BaseModel):
    topic: str = Field(
        ...,
        description="The subject or topic to be researched.",
        examples=["Emerging trends in AI for Education 2026"]
    )
    session_id: str | None = Field(
        default=None,
        description="Optional session identifier for conversation continuity."
    )


# Pydantic schema for response body
class ResearchResponse(BaseModel):
    status: str
    session_id: str
    topic: str
    report: str


@app.get("/")
def serve_dashboard():
    """Serves the interactive web interface dashboard."""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "service": "DeepResearcher ADK API",
        "model": "Gemini Flash (via Google ADK)",
        "docs_url": "/docs"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint providing service status and metadata."""
    return {
        "status": "online",
        "service": "DeepResearcher ADK API",
        "model": "Gemini Flash (via Google ADK)",
        "version": "1.1.0"
    }


@app.post("/api/v1/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest):
    """
    Triggers an autonomous research workflow:
    The agent searches the web, fetches articles, and returns a synthesized report.
    """
    session_id = request.session_id or f"session_{uuid.uuid4().hex[:8]}"

    try:
        report = await execute_research(topic=request.topic, session_id=session_id)
        return ResearchResponse(
            status="success",
            session_id=session_id,
            topic=request.topic,
            report=report
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during agent execution: {str(e)}"
        )


if __name__ == "__main__":
    # Start the Uvicorn ASGI server on port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
