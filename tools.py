"""
tools.py - Autonomous Research Agent Tools.

In Google ADK, standard Python functions with type hints and docstrings
are automatically converted into Function Tools for Gemini models.
"""

from ddgs import DDGS
import requests
from bs4 import BeautifulSoup


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches the live web for real-time information using DuckDuckGo.

    Args:
        query: The search term or topic (e.g., 'latest AI trends in education 2026').
        max_results: Maximum number of search results to retrieve (default is 5).

    Returns:
        A list of dictionaries containing title, url, and snippet for each result.
    """
    results = []
    try:
        with DDGS() as ddgs:
            raw_results = ddgs.text(query, max_results=max_results)
            for r in raw_results:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        results.append({"error": f"Search execution failed: {str(e)}"})

    return results


def fetch_web_content(url: str) -> str:
    """
    Visits a web page and extracts its cleaned text content.
    Used by the agent for deep reading and synthesis of specific sources.

    Args:
        url: The full URL of the webpage to scrape.

    Returns:
        Cleaned text content of the page (truncated to avoid exceeding context window).
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()

        # Parse and strip HTML tags
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove non-content elements
        for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            element.extract()

        text = soup.get_text(separator=" ", strip=True)
        # Limit text size to ~4000 characters for token efficiency
        return text[:4000]
    except Exception as e:
        return f"Failed to fetch webpage content: {str(e)}"
