"""
test_api.py - Integration and endpoint tests for FastAPI server.
"""

from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Verify the health check endpoint returns 200 OK and online status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "service" in data


def test_dashboard_endpoint():
    """Verify root path serves the web UI index.html."""
    response = client.get("/")
    assert response.status_code == 200
    assert "DeepResearcher ADK" in response.text


def test_research_endpoint_success():
    """Verify POST /api/v1/research invokes agent and returns structured response."""
    mock_report = "# Research Report\n\nKey findings on AI agents."

    with patch("main.execute_research", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_report

        payload = {"topic": "AI in Education 2026", "session_id": "test_session_42"}
        response = client.post("/api/v1/research", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["session_id"] == "test_session_42"
        assert data["report"] == mock_report
        mock_exec.assert_awaited_once_with(topic="AI in Education 2026", session_id="test_session_42")


def test_research_endpoint_validation_error():
    """Verify endpoint rejects invalid payloads missing required topic field."""
    response = client.post("/api/v1/research", json={})
    assert response.status_code == 422  # Unprocessable Entity
