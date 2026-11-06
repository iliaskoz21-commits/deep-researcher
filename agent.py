"""
agent.py - Google ADK Research Agent Configuration.

Binds the Gemini Flash model to custom tools (web search and webpage scraper)
and orchestrates multi-step autonomous research via Google ADK Runner.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import custom tools
from tools import search_web, fetch_web_content

# Load environment variables from .env
load_dotenv()

# System instruction defining agent behavior and research methodology
RESEARCHER_INSTRUCTION = """
You are an expert Autonomous Research AI Agent.
Your objective is to conduct in-depth, objective, and high-quality research on the user's requested topic.

Follow this methodology:
1. Use the `search_web` tool to discover recent, relevant, and authoritative sources.
2. When necessary for deeper insights or verification, use `fetch_web_content` to read promising sources.
3. Critically analyze all findings, eliminating promotional filler and hallucinations.
4. Synthesize a comprehensive, well-structured Markdown report containing:
   - **Executive Summary**
   - **Key Findings & In-depth Technical Details**
   - **Critical Analysis & Industry Outlook**
   - **References & Sources** (with direct markdown links to original URLs)
"""


def create_research_agent(model_name: str = "gemini-2.5-flash") -> Agent:
    """
    Factory function returning a configured Google ADK Agent instance.
    
    Args:
        model_name: The Gemini model identifier (default: gemini-2.5-flash).
        
    Returns:
        Configured Agent instance.
    """
    return Agent(
        name="deep_researcher",
        model=model_name,
        instruction=RESEARCHER_INSTRUCTION,
        description="Autonomous research specialist that browses and analyzes web data.",
        tools=[search_web, fetch_web_content],
    )


# Session service managing conversation history and transient state in memory
session_service = InMemorySessionService()


async def execute_research(topic: str, session_id: str = "default_session") -> str:
    """
    Executes a complete autonomous research run on the requested topic.

    Args:
        topic: The user's query or research subject.
        session_id: Unique session identifier for maintaining multi-turn context.

    Returns:
        The final synthesized Markdown report from the agent.
    """
    # Create or retrieve the session
    try:
        await session_service.create_session(
            app_name="deep_researcher_app",
            user_id="research_user",
            session_id=session_id
        )
    except Exception:
        # Session already exists
        pass

    agent = create_research_agent()
    runner = Runner(
        agent=agent,
        app_name="deep_researcher_app",
        session_service=session_service
    )

    # User input message dispatched to the agent
    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=f"Conduct thorough research on: {topic}")]
    )

    final_report = ""

    # Execute the agent loop (ADK automatically handles LLM reasoning and tool calls)
    async for event in runner.run_async(
        user_id="research_user",
        session_id=session_id,
        new_message=user_message
    ):
        # Check if the event contains the agent's final synthesized response
        if event.is_final_response():
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        final_report += part.text

    return final_report
