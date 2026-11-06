"""
main.py - Flask Web Application for DeepResearcher.

Provides a clean Pythonic web interface using Jinja2 templates,
and REST endpoints to run autonomous research workflows using Google ADK & Gemini Flash.
"""

from flask import Flask, render_template, request, jsonify
import markdown
import asyncio
import os
from agent import execute_research

# Initialize Flask application
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main web interface route.
    Handles GET to display the form and POST to execute the research agent.
    """
    topic = ""
    report_html = None
    error = None

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()

        if not topic:
            error = "Please provide a research topic."
        else:
            try:
                # Run the asynchronous ADK research agent
                raw_report = asyncio.run(execute_research(topic=topic))

                # Convert Markdown to HTML server-side
                report_html = markdown.markdown(
                    raw_report,
                    extensions=["fenced_code", "tables"]
                )
            except Exception as e:
                error = f"Agent execution failed: {str(e)}"

    return render_template("index.html", topic=topic, report_html=report_html, error=error)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint returning service status in JSON."""
    return jsonify({
        "status": "online",
        "service": "DeepResearcher Flask Service",
        "framework": "Flask 3.x",
        "model": "Gemini Flash (via Google ADK)"
    })


@app.route("/api/v1/research", methods=["POST"])
def api_research():
    """
    JSON REST API endpoint for external clients and programmatic requests.
    """
    data = request.get_json() or {}
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"status": "error", "message": "Missing 'topic' field"}), 400

    session_id = data.get("session_id", "default_session")

    try:
        raw_report = asyncio.run(execute_research(topic=topic, session_id=session_id))
        return jsonify({
            "status": "success",
            "topic": topic,
            "session_id": session_id,
            "report": raw_report
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # Run the Flask development server on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
