from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List

import fitz  # PyMuPDF
from linkedin_jobs_scraper import LinkedinScraper, events, query
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


logger = logging.getLogger("linkedin_agent.scraper")

JOB_RESULTS: List[Dict[str, Any]] = []


def _on_data(data) -> None:
    JOB_RESULTS.append(
        {
            "title": data.title,
            "company": data.company,
            "location": data.location,
            "description": data.description,
            "link": data.link,
            "date": data.date,
        }
    )


def _on_error(error) -> None:
    logger.error("LinkedIn scraper error: %r", error)


def _on_end() -> None:
    logger.info("LinkedIn scraper run completed with %d results", len(JOB_RESULTS))


def scrape_linkedin_jobs(
    search_term: str,
    location: str = "Remote",
    num_jobs: int = 10,
) -> List[Dict[str, Any]]:
    """
    Scrape LinkedIn job postings using `linkedin-jobs-scraper`.

    Returns a list of dictionaries with title, company, location,
    description, link, and date.

    Notes on reliability:
    - Filters are intentionally kept broad (no experience/type filter)
      so that scraping succeeds more often.
    - Page load timeout is increased to better tolerate slow responses.
    - If the LI_AT_COOKIE environment variable is not set, scraping
      runs in anonymous mode which is much more likely to be blocked
      or return zero results.
    """
    global JOB_RESULTS
    JOB_RESULTS = []

    li_at = os.getenv("LI_AT_COOKIE")
    if not li_at:
        logger.warning(
            "LI_AT_COOKIE is not set; running LinkedIn scrape in anonymous mode. "
            "Set LI_AT_COOKIE in your .env for more reliable results."
        )

    page_timeout_env = os.getenv("LINKEDIN_PAGE_TIMEOUT_SECONDS")
    try:
        page_timeout = int(page_timeout_env) if page_timeout_env else 60
    except ValueError:
        logger.warning(
            "Invalid LINKEDIN_PAGE_TIMEOUT_SECONDS value %r; falling back to 60 seconds",
            page_timeout_env,
        )
        page_timeout = 60

    logger.info(
        "Starting LinkedIn scrape",
        extra={
            "search_term": search_term,
            "location": location,
            "num_jobs": num_jobs,
            "anonymous_mode": not bool(li_at),
            "page_timeout_seconds": page_timeout,
        },
    )

    scraper = LinkedinScraper(
        chrome_executable_path=None,
        headless=True,
        max_workers=1,
        slow_mo=0.5,
        page_load_timeout=page_timeout,
    )

    scraper.on(events.Events.DATA, _on_data)
    scraper.on(events.Events.ERROR, _on_error)
    scraper.on(events.Events.END, _on_end)

    queries = [
        query.Query(
            query=search_term,
            options=query.QueryOptions(
                locations=[location],
                apply_link=True,
                limit=num_jobs,
                # No additional filters to maximize the chance of hits.
                filters=None,
            ),
        ),
    ]

    scraper.run(queries)
    # small delay to allow background workers to flush
    time.sleep(2)

    logger.info("LinkedIn scrape finished with %d jobs", len(JOB_RESULTS))
    return JOB_RESULTS.copy()


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract raw text from a PDF resume using PyMuPDF.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def resume_job_desc_match(resume_text: str, job_desc: str) -> float:
    """
    Compute a simple cosine-similarity score between resume and job description.

    Returns a percentage similarity (0.0 - 100.0).
    """
    content = [resume_text, job_desc]
    cv = CountVectorizer()
    matrix = cv.fit_transform(content)
    similarity_matrix = cosine_similarity(matrix)
    match_percentage = float(similarity_matrix[0][1] * 100.0)
    return round(match_percentage, 2)


