from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # So LI_AT_COOKIE is available when linkedin-jobs-scraper is imported

from linkedin_agent.config import load_settings
from linkedin_agent import run_linkedin_agent_workflow
from linkedin_agent.logging_utils import configure_logging
from linkedin_agent.query_intent import parse_search_intent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Production-ready LinkedIn AI Agent for resume/job matching."
    )
    parser.add_argument(
        "--resume",
        required=True,
        help="Path to the candidate resume PDF.",
    )
    parser.add_argument(
        "--query",
        required=False,
        help='Structured job search query, e.g. "AI Engineer". If omitted, use --natural-query.',
    )
    parser.add_argument(
        "--location",
        default=None,
        help='Job location (default: value from LINKEDIN_DEFAULT_LOCATION, typically "Remote").',
    )
    parser.add_argument(
        "--natural-query",
        default=None,
        help=(
            "Natural-language description of what to search for, e.g. "
            "'look for ai engineer roles with no experience in Hyderabad posted in the last 24 hours'. "
            "When provided, the agent parses this into structured search parameters."
        ),
    )
    parser.add_argument(
        "--num-jobs",
        type=int,
        default=None,
        help="Number of jobs to scrape and score (default from LINKEDIN_DEFAULT_NUM_JOBS).",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of top matching jobs to generate suggestions for.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Optional path to write the structured results as JSON.",
    )
    return parser.parse_args()


def main() -> None:
    configure_logging()

    args = parse_args()
    settings = load_settings()

    logger = logging.getLogger("linkedin_agent")

    if args.natural_query:
        intent = parse_search_intent(args.natural_query, settings)
        job_query = intent.job_query
        location = intent.location or args.location
        num_jobs = intent.limit or args.num_jobs
        top_k = intent.top_k or args.top_k
        max_job_age_days = intent.max_job_age_days

        logger.info(
            "Parsed natural-language search intent",
            extra=intent.dict(),
        )
    else:
        if not args.query:
            raise SystemExit("Either --query or --natural-query must be provided.")
        job_query = args.query
        location = args.location
        num_jobs = args.num_jobs
        top_k = args.top_k
        max_job_age_days = None

    logger.info(
        "Starting LinkedIn agent workflow",
        extra={
            "resume_path": str(args.resume),
            "job_query": job_query,
            "location": location,
            "num_jobs": num_jobs,
            "top_k": top_k,
            "max_job_age_days": max_job_age_days,
        },
    )

    results = run_linkedin_agent_workflow(
        settings=settings,
        resume_path=args.resume,
        job_query=job_query,
        location=location,
        num_jobs=num_jobs,
        top_k=top_k,
        max_job_age_days=max_job_age_days,
    )

    if args.output_json:
        args.output_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n--- Top Matching Jobs and Personalized Suggestions ---\n")
    for job in results:
        print(f"[{job['title']} at {job['company']}] (Score: {job['score']}%)")
        print(f"Location: {job['location']}")
        print(f"Link: {job['link']}")
        print("Improvement Suggestions:\n", job["suggestions"])
        print("-" * 80)


if __name__ == "__main__":
    main()

