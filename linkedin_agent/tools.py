from __future__ import annotations

import time
from typing import List, Dict, Any

import fitz  # PyMuPDF
from linkedin_jobs_scraper import LinkedinScraper, events, query, filters
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
    print("[ON_ERROR]", error)


def _on_end() -> None:
    print("[END]")


def scrape_linkedin_jobs(
    search_term: str,
    location: str = "Remote",
    num_jobs: int = 10,
) -> List[Dict[str, Any]]:
    """
    Scrape LinkedIn job postings using `linkedin-jobs-scraper`.

    Returns a list of dictionaries with title, company, location,
    description, link, and date.
    """
    global JOB_RESULTS
    JOB_RESULTS = []

    scraper = LinkedinScraper(
        chrome_executable_path=None,
        headless=True,
        max_workers=1,
        slow_mo=0.5,
        page_load_timeout=20,
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
                filters=query.QueryFilters(
                    experience=[filters.ExperienceLevelFilters.ENTRY_LEVEL],
                    type=[filters.TypeFilters.FULL_TIME],
                ),
            ),
        ),
    ]

    scraper.run(queries)
    # small delay to allow background workers to flush
    time.sleep(2)
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

