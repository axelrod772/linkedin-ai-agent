"""
Production-ready LinkedIn agent package.

Exposes high-level workflow helpers for scraping jobs,
matching them against a resume, and generating
LLM-powered improvement suggestions.
"""

from .agent import run_linkedin_agent_workflow

__all__ = ["run_linkedin_agent_workflow"]

