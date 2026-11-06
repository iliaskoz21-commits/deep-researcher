"""
test_tools.py - Unit tests for autonomous research tools.
"""

from unittest.mock import patch, MagicMock
from tools import search_web, fetch_web_content


def test_search_web_structure():
    """Verify search_web returns formatted dictionaries with expected keys."""
    mock_ddgs_results = [
        {
            "title": "Python 3.12 Overview",
            "href": "https://python.org/doc/3.12",
            "body": "Python 3.12 includes performance improvements."
        }
    ]

    with patch("tools.DDGS") as MockDDGS:
        mock_instance = MagicMock()
        mock_instance.text.return_value = mock_ddgs_results
        MockDDGS.return_value.__enter__.return_value = mock_instance

        results = search_web("python 3.12", max_results=1)

        assert len(results) == 1
        assert results[0]["title"] == "Python 3.12 Overview"
        assert results[0]["url"] == "https://python.org/doc/3.12"
        assert "performance" in results[0]["snippet"]


def test_fetch_web_content_cleaning():
    """Verify HTML tags, scripts, and navigation elements are stripped properly."""
    sample_html = """
    <html>
        <head><title>Test Page</title><style>.test { color: red; }</style></head>
        <body>
            <nav><a href="/">Home</a></nav>
            <script>console.log("tracker");</script>
            <article>
                <h1>Deep Learning Advances</h1>
                <p>Autonomous agents are transforming software engineering.</p>
            </article>
            <footer>Footer copyright 2026</footer>
        </body>
    </html>
    """

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        text = fetch_web_content("https://example.com/article")

        assert "Deep Learning Advances" in text
        assert "Autonomous agents are transforming software engineering" in text
        assert "console.log" not in text
        assert "Footer copyright" not in text
