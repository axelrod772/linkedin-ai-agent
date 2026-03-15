from __future__ import annotations

from typing import Optional, Literal

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate

from .config import Settings


class SearchIntent(BaseModel):
    """
    Structured representation of a natural-language job search request.
    """

    job_query: str = Field(
        ...,
        description="Primary job title or role to search for, e.g. 'AI Engineer'.",
    )
    location: Optional[str] = Field(
        None,
        description="City/region or 'Remote' if explicitly requested.",
    )
    experience_level: Literal[
        "no_experience",
        "entry",
        "mid",
        "senior",
        "any",
    ] = Field(
        "any",
        description="Seniority or experience level requested.",
    )
    max_job_age_days: Optional[int] = Field(
        None,
        description="Only consider jobs posted in the last N days, e.g. 1 for last 24 hours.",
    )
    limit: Optional[int] = Field(
        None,
        description="Maximum number of jobs to scrape/evaluate.",
    )
    top_k: Optional[int] = Field(
        None,
        description="Number of top matching jobs to return after scoring.",
    )


def parse_search_intent(
    natural_query: str,
    settings: Settings,
) -> SearchIntent:
    """
    Parse a natural-language job search description into structured parameters.

    Example input:
    "This is my resume, can you look for ai developer / ai engineer roles with no experience in Hyderabad
     which were uploaded in the last 24 hours?"
    """
    llm = ChatOpenAI(
        model=settings.openai_model_name,
        temperature=0.1,
    )

    parser = PydanticOutputParser(pydantic_object=SearchIntent)
    format_instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_template(
        (
            "You are an AI assistant that converts natural-language job search requests into structured parameters.\n\n"
            "User request:\n"
            "{natural_query}\n\n"
            "Your task:\n"
            "- Identify the primary job title or role (job_query).\n"
            "- Identify the location (city/region or 'Remote'). If none is given, leave it null.\n"
            "- Infer the experience_level from phrases like 'no experience', 'fresher', 'junior', 'mid', "
            "'5+ years', 'senior', etc. Map them into one of: 'no_experience', 'entry', 'mid', 'senior', or 'any'.\n"
            "- If the user mentions a time window such as 'last 24 hours', 'last day', 'last 3 days', 'last week', "
            "set max_job_age_days accordingly (1, 3, 7, etc.). If not mentioned, leave it null.\n"
            "- If the user hints at how many jobs to consider (e.g. 'top 10 jobs'), set limit; otherwise leave null.\n"
            "- If the user hints at how many best matches they want (e.g. 'show me the top 3'), set top_k; "
            "otherwise leave null.\n\n"
            "Return ONLY a JSON object that conforms to this schema:\n"
            "{format_instructions}\n"
        )
    )

    chain = prompt | llm | parser
    intent: SearchIntent = chain.invoke(
        {"natural_query": natural_query, "format_instructions": format_instructions}
    )

    # Apply simple defaults if the model leaves fields unset.
    if intent.max_job_age_days is None:
        intent.max_job_age_days = settings.max_job_age_days
    if intent.limit is None:
        intent.limit = settings.default_num_jobs
    if intent.top_k is None:
        intent.top_k = settings.agent_default_top_k
    if intent.location is None:
        intent.location = settings.default_location

    return intent

