from __future__ import annotations

import os
import logging
from typing import List, Dict, Any
from langchain_classic.agents import AgentExecutor, create_openai_functions_agent
from langchain_classic.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from .config import Settings
from .memory import JSONMemoryStore
from .sample_jobs_data import get_sample_jobs
from .tools import scrape_linkedin_jobs, extract_text_from_pdf, resume_job_desc_match
from .vector_memory import get_vector_store, add_profile_document, find_similar_profiles


logger = logging.getLogger("linkedin_agent.agent")


class OutreachPlan(BaseModel):
    """
    Structured plan for a LinkedIn outreach message.
    """

    subject: str = Field(..., description="Subject line or opening hook for the message.")
    message: str = Field(..., description="Full LinkedIn message body tailored to the recipient.")
    strategy: str = Field(..., description="Short explanation of why this approach was chosen.")
    tone: str = Field(..., description="The dominant tone to use, e.g. 'casual', 'professional', or 'enthusiastic'.")
    industry: str = Field(..., description="The recipient's primary industry, inferred from their profile.")


def plan_outreach(profile_summary: str) -> OutreachPlan:
    """
    Core reasoning loop for generating an outreach plan from a profile summary.

    This is used both by the LangChain tool and the FastAPI endpoint.
    """
    parser = PydanticOutputParser(pydantic_object=OutreachPlan)
    format_instructions = parser.get_format_instructions()

    llm = ChatOpenAI(temperature=0.4)
    prompt = ChatPromptTemplate.from_template(
        (
            "You are an AI sales assistant crafting highly personalized LinkedIn messages.\n\n"
            "First, read the profile summary below and infer the person's primary industry, seniority, "
            "and likely interests. Then choose the most appropriate tone for the outreach message "
            "(for example, 'friendly and casual' for startup engineers, or 'concise and formal' for "
            "enterprise executives).\n\n"
            "Profile summary:\n"
            "{profile_summary}\n\n"
            "Your response must strictly follow this JSON schema:\n"
            "{format_instructions}\n\n"
            "- The `subject` should be a short, compelling opening line.\n"
            "- The `message` should be a complete LinkedIn connection/request message.\n"
            "- The `strategy` should briefly explain *why* you chose this industry framing and tone.\n"
            "- The `tone` must be a concrete label such as 'casual', 'professional', or 'enthusiastic'.\n"
            "- The `industry` should be a single high-level label such as 'SaaS', 'Fintech', or 'Healthcare AI'."
        )
    )

    chain = prompt | llm | parser
    plan: OutreachPlan = chain.invoke({"profile_summary": profile_summary})

    logger.info(
        "Generated outreach plan",
        extra={
            "subject": plan.subject,
            "tone": plan.tone,
            "industry": plan.industry,
            "strategy": plan.strategy,
        },
    )

    return plan


def _build_tools(memory: JSONMemoryStore) -> List[Tool]:
    """
    LangChain tools used by the OpenAI Functions agent.
    """

    def get_profile_history(profile_id: str) -> str:
        interactions = memory.get_interactions(profile_id)
        if not interactions:
            return "No prior interactions for this profile."

        lines = []
        for idx, inter in enumerate(interactions, start=1):
            lines.append(
                f"{idx}. {inter.job_title} at {inter.company} "
                f"(score={inter.score}) -> {inter.suggestions}"
            )
        return "\n".join(lines)

    def linkedin_messenger(profile_summary: str) -> str:
        """
        Reason about a LinkedIn recipient profile and synthesize
        an outreach message with explicit subject, message, and strategy.
        """
        plan = plan_outreach(profile_summary)
        # Return as JSON string so the tool output is easy to consume.
        return plan.json()

    return [
        Tool(
            name="scrape_linkedin_jobs",
            func=scrape_linkedin_jobs,
            description=(
                "Scrape LinkedIn for jobs. "
                "Inputs: search_term (str), location (str), num_jobs (int)."
            ),
        ),
        Tool(
            name="get_profile_history",
            func=get_profile_history,
            description=(
                "Retrieve prior suggestions for a given profile_id "
                "to maintain long-term memory."
            ),
        ),
        Tool(
            name="linkedin_messenger",
            func=linkedin_messenger,
            description=(
                "Analyze a LinkedIn profile summary and synthesize a JSON object "
                "with subject, message, tone, industry, and strategy fields for outreach."
            ),
        ),
    ]


def _build_agent(settings: Settings, memory: JSONMemoryStore) -> AgentExecutor:
    """
    Create an OpenAI Functions agent that can call the registered tools
    and reason about how to update or query memory.
    """
    if not settings.openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Please configure it in your environment or .env file."
        )

    llm = ChatOpenAI(
        model=settings.openai_model_name,
        temperature=0.2,
    )

    tools = _build_tools(memory)

    system_prompt = (
        "You are an AI career coach and LinkedIn job-matching assistant. "
        "You help AI/ML engineers tailor their resume to specific jobs.\n\n"
        "You have access to tools that can scrape LinkedIn jobs and that "
        "let you read/write persistent profile history. Use this memory to "
        "avoid repeating yourself and to refine suggestions over time. "
        "You can call a tool to view prior interactions for this profile id.\n\n"
        "When asked for suggestions, return:\n"
        "- A short justification (1–2 sentences) of the match quality.\n"
        "- Bullet points with concrete resume improvements.\n"
        "- Any missing keywords or skills that should be added."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            # Required by create_openai_functions_agent so it can inject tool call traces.
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


def _sample_jobs(search_term: str, location: str) -> List[Dict[str, Any]]:
    """
    Fallback sample jobs used when live scraping fails or returns nothing.
    Returns 100+ India-based roles (companies and locations) so any resume gets a match.
    """
    return get_sample_jobs(search_term, location)


def _job_age_in_days(date_str: str) -> int | None:
    """
    Best-effort conversion of LinkedIn job 'date' strings into an age in days.

    Handles values like 'Today', 'Yesterday', '3 days ago', or returns None
    if the format is unrecognized.
    """
    text = str(date_str).strip().lower()
    if not text:
        return None
    if "today" in text or "just now" in text:
        return 0
    if "yesterday" in text:
        return 1
    for token in text.split():
        if token.isdigit():
            try:
                return int(token)
            except ValueError:
                return None
    return None


def run_linkedin_agent_workflow(
    settings: Settings,
    resume_path: str,
    job_query: str,
    location: str | None = None,
    num_jobs: int | None = None,
    top_k: int | None = None,
    max_job_age_days: int | None = None,
) -> List[Dict[str, Any]]:
    """
    High-level orchestration of the LinkedIn agent:

    1. Load resume and compute a stable profile id.
    2. Scrape LinkedIn jobs.
    3. Score jobs using a traditional cosine-similarity baseline.
    4. For the top-k jobs, call the LLM agent to generate targeted
       improvement suggestions and persist them to JSON memory.
    """
    memory = JSONMemoryStore(settings.memory_path)
    vector_store = get_vector_store(settings)
    agent = _build_agent(settings, memory)

    resume_text = extract_text_from_pdf(resume_path)
    profile_id = memory.profile_id_from_resume(resume_text)

    location = location or settings.default_location
    num_jobs = num_jobs or settings.default_num_jobs
    top_k = top_k or settings.agent_default_top_k
    max_job_age_days = max_job_age_days or settings.max_job_age_days

    logger.info(
        "Scraping LinkedIn jobs",
        extra={"job_query": job_query, "location": location, "num_jobs": num_jobs},
    )

    try:
        scraped_jobs = scrape_linkedin_jobs(
            search_term=job_query,
            location=location,
            num_jobs=num_jobs,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[warning] LinkedIn scrape failed with error: {exc!r}")
        scraped_jobs = []

    if not scraped_jobs:
        use_sample = os.getenv("LINKEDIN_USE_SAMPLE_JOBS_IF_EMPTY", "true").lower() == "true"
        if use_sample:
            print("[info] No jobs scraped from LinkedIn; falling back to sample jobs.")
            scraped_jobs = _sample_jobs(job_query, location)
        else:
            raise RuntimeError("No jobs scraped from LinkedIn. Try a different query or location.")

    # Optionally filter jobs by recency if we can interpret the 'date' field.
    if max_job_age_days is not None:
        filtered: List[Dict[str, Any]] = []
        for job in scraped_jobs:
            age = _job_age_in_days(job.get("date", ""))
            if age is None or age <= max_job_age_days:
                filtered.append(job)
        if filtered:
            scraped_jobs = filtered

    scored_jobs: List[Dict[str, Any]] = []
    for job in scraped_jobs:
        score = resume_job_desc_match(resume_text, job["description"])
        scored_jobs.append(
            {
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "description": job["description"],
                "link": job["link"],
                "date": job["date"],
                "score": score,
            }
        )

    scored_jobs.sort(key=lambda j: j["score"], reverse=True)
    top_jobs = scored_jobs[:top_k]

    results: List[Dict[str, Any]] = []
    for job in top_jobs:
        # Build a rich natural-language input so the agent can decide
        # when to consult memory and how to respond.
        # Store this interaction as a semantic document in Chroma so
        # future runs can recall similar profiles / roles.
        profile_doc_text = (
            f"Job: {job['title']} at {job['company']} (Location: {job['location']})\n"
            f"Description:\n{job['description']}\n"
        )
        profile_metadata = {
            "profile_id": profile_id,
            "job_link": job["link"],
            "job_title": job["title"],
            "company": job["company"],
            "type": "job_profile",
        }
        add_profile_document(
            vector_store=vector_store,
            text=profile_doc_text,
            metadata=profile_metadata,
            doc_id=f"{profile_id}:{job['link']}",
        )

        similar_profiles = find_similar_profiles(
            vector_store=vector_store,
            query_text=job["description"],
            k=3,
        )
        similar_snippets = []
        for idx, (text, meta) in enumerate(similar_profiles, start=1):
            ref_company = meta.get("company", "Unknown Company")
            ref_title = meta.get("job_title", "Unknown Title")
            similar_snippets.append(f"{idx}. {ref_title} at {ref_company}")

        similar_text_block = (
            "I see this job is similar to previous leads:\n"
            + "\n".join(similar_snippets)
            if similar_snippets
            else "No closely similar prior leads were found in memory."
        )

        agent_input = (
            "You are analyzing a candidate's resume against a specific job.\n\n"
            f"Profile id: {profile_id}\n"
            f"Job title: {job['title']}\n"
            f"Company: {job['company']}\n"
            f"Location: {job['location']}\n"
            f"Link: {job['link']}\n"
            f"Relevance score (baseline): {job['score']}%\n\n"
            f"{similar_text_block}\n\n"
            "Resume text:\n"
            f"{resume_text}\n\n"
            "Job description:\n"
            f"{job['description']}\n\n"
            "First, if helpful, call `get_profile_history` to see prior "
            "interactions for this profile. Then, provide tailored suggestions "
            "to improve the resume for this job. Your answer should include "
            "a brief rationale and concrete bullet points."
        )

        logger.info(
            "Invoking agent for job",
            extra={
                "profile_id": profile_id,
                "job_title": job["title"],
                "company": job["company"],
                "baseline_score": job["score"],
            },
        )

        agent_output = agent.invoke(
            {
                "input": agent_input,
                "chat_history": [],
            }
        )

        suggestions_text = agent_output.get("output", "")

        logger.info(
            "Agent completed for job",
            extra={
                "profile_id": profile_id,
                "job_title": job["title"],
                "company": job["company"],
            },
        )

        memory.add_interaction(
            profile_id=profile_id,
            job_link=job["link"],
            job_title=job["title"],
            company=job["company"],
            score=job["score"],
            suggestions=suggestions_text,
        )

        results.append(
            {
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "link": job["link"],
                "date": job["date"],
                "score": job["score"],
                "suggestions": suggestions_text,
            }
        )

    return results

