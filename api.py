from __future__ import annotations

import logging
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from linkedin_agent.config import load_settings, Settings
from linkedin_agent.logging_utils import configure_logging
from linkedin_agent.vector_memory import get_vector_store, find_similar_profiles
from linkedin_agent.agent import plan_outreach, OutreachPlan


app = FastAPI(title="LinkedIn Outreach Agent API", version="1.0.0")

logger = logging.getLogger("linkedin_agent.api")

_settings: Optional[Settings] = None
_vector_store = None


class ProfileRequest(BaseModel):
    profile_summary: str


@app.on_event("startup")
def startup_event() -> None:
    """
    Initialize logging, configuration, and vector store on app startup.
    """
    global _settings, _vector_store

    configure_logging()
    _settings = load_settings()
    _vector_store = get_vector_store(_settings)

    logger.info("FastAPI application startup complete")


@app.post("/api/linkedin-messenger", response_model=OutreachPlan)
def linkedin_messenger_endpoint(payload: ProfileRequest) -> OutreachPlan:
    """
    Accept a LinkedIn profile summary and return a structured outreach plan.

    The endpoint:
    - Queries the ChromaDB vector store for similar prior profiles.
    - Augments the input summary with that context.
    - Runs the core reasoning loop to generate subject, message, tone,
      industry, and strategy as a Pydantic model.
    """
    if _settings is None or _vector_store is None:
        # This should not happen in normal operation because startup_event runs first.
        startup_event()

    logger.info("Received linkedin_messenger request")

    similar_profiles = find_similar_profiles(
        vector_store=_vector_store,
        query_text=payload.profile_summary,
        k=3,
    )

    similar_snippets = []
    for idx, (_text, meta) in enumerate(similar_profiles, start=1):
        ref_company = meta.get("company", "Unknown Company")
        ref_title = meta.get("job_title", "Unknown Title")
        similar_snippets.append(f"{idx}. {ref_title} at {ref_company}")

    if similar_snippets:
        memory_context = (
            "I see you are in a similar space as these previous leads:\n"
            + "\n".join(similar_snippets)
            + "\n\nOriginal profile summary:\n"
            + payload.profile_summary
        )
    else:
        memory_context = (
            "No closely similar prior leads were found in memory.\n\n"
            "Original profile summary:\n"
            + payload.profile_summary
        )

    plan = plan_outreach(memory_context)
    logger.info(
        "linkedin_messenger plan generated",
        extra={
            "subject": plan.subject,
            "tone": plan.tone,
            "industry": plan.industry,
        },
    )
    return plan


from __future__ import annotations

import logging
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from linkedin_agent.config import load_settings, Settings
from linkedin_agent.logging_utils import configure_logging
from linkedin_agent.vector_memory import get_vector_store, find_similar_profiles
from linkedin_agent.agent import plan_outreach, OutreachPlan


app = FastAPI(title="LinkedIn Outreach Agent API", version="1.0.0")

logger = logging.getLogger("linkedin_agent.api")

_settings: Optional[Settings] = None
_vector_store = None


class ProfileRequest(BaseModel):
    profile_summary: str


@app.on_event("startup")
def startup_event() -> None:
    """
    Initialize logging, configuration, and vector store on app startup.
    """
    global _settings, _vector_store

    configure_logging()
    _settings = load_settings()
    _vector_store = get_vector_store(_settings)

    logger.info("FastAPI application startup complete")


@app.post("/api/linkedin-messenger", response_model=OutreachPlan)
def linkedin_messenger_endpoint(payload: ProfileRequest) -> OutreachPlan:
    """
    Accept a LinkedIn profile summary and return a structured outreach plan.

    The endpoint:
    - Queries the ChromaDB vector store for similar prior profiles.
    - Augments the input summary with that context.
    - Runs the core reasoning loop to generate subject, message, tone,
      industry, and strategy as a Pydantic model.
    """
    if _settings is None or _vector_store is None:
        # This should not happen in normal operation because startup_event runs first.
        startup_event()

    logger.info("Received linkedin_messenger request")

    similar_profiles = find_similar_profiles(
        vector_store=_vector_store,
        query_text=payload.profile_summary,
        k=3,
    )

    similar_snippets = []
    for idx, (_text, meta) in enumerate(similar_profiles, start=1):
        ref_company = meta.get("company", "Unknown Company")
        ref_title = meta.get("job_title", "Unknown Title")
        similar_snippets.append(f"{idx}. {ref_title} at {ref_company}")

    if similar_snippets:
        memory_context = (
            "I see you are in a similar space as these previous leads:\n"
            + "\n".join(similar_snippets)
            + "\n\nOriginal profile summary:\n"
            + payload.profile_summary
        )
    else:
        memory_context = (
            "No closely similar prior leads were found in memory.\n\n"
            "Original profile summary:\n"
            + payload.profile_summary
        )

    plan = plan_outreach(memory_context)
    logger.info(
        "linkedin_messenger plan generated",
        extra={
            "subject": plan.subject,
            "tone": plan.tone,
            "industry": plan.industry,
        },
    )
    return plan


