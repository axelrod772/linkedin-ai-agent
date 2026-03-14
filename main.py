from __future__ import annotations

import argparse
import json
from pathlib import Path

from linkedin_agent.config import load_settings
from linkedin_agent import run_linkedin_agent_workflow


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
        required=True,
        help='Job search query, e.g. "AI Engineer" or "Machine Learning Engineer".',
    )
    parser.add_argument(
        "--location",
        default=None,
        help='Job location (default: value from LINKEDIN_DEFAULT_LOCATION, typically "Remote").',
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
    args = parse_args()
    settings = load_settings()

    results = run_linkedin_agent_workflow(
        settings=settings,
        resume_path=args.resume,
        job_query=args.query,
        location=args.location,
        num_jobs=args.num_jobs,
        top_k=args.top_k,
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

