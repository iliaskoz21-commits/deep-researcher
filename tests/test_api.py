"""
test_api.py - Unit and integration tests for Flask web app.
"""

import pytest
from unittest.mock import patch, AsyncMock
from main import app


@pytest.fixture
def client():
    """Configures the Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Verify GET /api/health returns online JSON status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "online"
    assert "Flask" in data["framework"]


def test_index_get(client):
    """Verify GET / renders the Jinja2 HTML form."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"DeepResearcher" in response.data
    assert b"<form" in response.data


def test_index_post_success(client):
    """Verify POST / triggers research and renders markdown result."""
    sample_report = "## Key Findings\n\n- AI enhances personalized learning."

    with patch("main.execute_research", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = sample_report

        response = client.post("/", data={"topic": "AI in High School"})
        assert response.status_code == 200
        assert b"Synthesized Research Report" in response.data
        assert b"AI enhances personalized learning" in response.data


def test_api_v1_research_endpoint(client):
    """Verify POST /api/v1/research returns JSON for external callers."""
    with patch("main.execute_research", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = "Detailed agent findings"

        response = client.post("/api/v1/research", json={"topic": "Google ADK Agents"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        assert data["report"] == "Detailed agent findings"
