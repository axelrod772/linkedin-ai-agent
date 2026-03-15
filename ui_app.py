from __future__ import annotations

from pathlib import Path
import logging
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # So LI_AT_COOKIE is available when linkedin-jobs-scraper is imported

from linkedin_agent import run_linkedin_agent_workflow
from linkedin_agent.config import load_settings
from linkedin_agent.logging_utils import configure_logging
from linkedin_agent.vector_memory import get_vector_store, find_similar_profiles
from linkedin_agent.agent import plan_outreach
from linkedin_agent.query_intent import parse_search_intent


def main() -> None:
    configure_logging()
    logger = logging.getLogger("linkedin_agent.ui")

    st.set_page_config(page_title="LinkedIn AI Agent", layout="wide")
    st.title("LinkedIn AI Agent – Resume & Job Match")
    st.markdown(
        "Upload your resume, describe what you want in plain language, and the agent will "
        "analyze realistic AI/ML job descriptions to suggest concrete improvements."
    )

    config_col, outreach_col = st.columns([2, 1])

    with config_col:
        st.subheader("Job search configuration")
        query_default = "AI Engineer"
        job_query = st.text_input("Target role / query", value=query_default)
        location = st.text_input("Location", value="Remote")
        top_k = st.slider("Top matching jobs", min_value=1, max_value=5, value=3)
        max_age_days = st.slider(
            "Only include jobs from last N days",
            min_value=1,
            max_value=30,
            value=3,
        )

        st.markdown("**Or describe your search in plain language:**")
        natural_query = st.text_area(
            "Natural language job request (optional)",
            placeholder=(
                "Example: Look for AI engineer roles with no experience in Hyderabad "
                "posted in the last 24 hours."
            ),
            height=80,
            key="natural_query",
        )

    with outreach_col:
        st.subheader("Outreach planner demo")
        outreach_profile = st.text_area(
            "Paste LinkedIn profile summary",
            height=150,
            key="outreach_profile_summary",
        )
        outreach_clicked = st.button(
            "Generate outreach plan",
            type="secondary",
            disabled=not outreach_profile.strip(),
            key="outreach_button",
        )

    if outreach_clicked and outreach_profile.strip():
        settings = load_settings()
        vector_store = get_vector_store(settings)
        similar_profiles = find_similar_profiles(
            vector_store=vector_store,
            query_text=outreach_profile,
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
                + outreach_profile
            )
        else:
            memory_context = (
                "No closely similar prior leads were found in memory.\n\n"
                "Original profile summary:\n"
                + outreach_profile
            )

        plan = plan_outreach(memory_context)

        st.subheader("Outreach plan")
        st.markdown("**Structured JSON response (subject, message, strategy, tone, industry):**")
        st.json(plan.dict())
        st.stop()

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    run_button_disabled = uploaded_file is None or (not job_query.strip() and not natural_query.strip())
    run_clicked = st.button("Run analysis", type="primary", disabled=run_button_disabled)

    if run_button_disabled:
        st.info("Upload a PDF resume and either enter a structured query or a natural-language request to begin.")

    if not run_clicked:
        return

    if uploaded_file is None:
        st.error("Please upload a resume PDF.")
        return

    settings = load_settings()

    # If the user provided a natural-language description, parse it into structured intent.
    parsed_intent = None
    if natural_query.strip():
        with st.spinner("Interpreting your natural language request..."):
            try:
                parsed_intent = parse_search_intent(natural_query, settings)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Failed to parse natural-language search intent")
                st.error(f"Could not interpret natural-language request: {exc}")
                return

        st.markdown("#### Interpreted search intent")
        st.json(parsed_intent.dict())

        job_query_effective = parsed_intent.job_query
        location_effective = parsed_intent.location or location
        num_jobs_effective = parsed_intent.limit
        top_k_effective = parsed_intent.top_k or top_k
        # UI slider takes precedence so demos are predictable.
        max_job_age_days_effective = max_age_days
    else:
        job_query_effective = job_query
        location_effective = location
        num_jobs_effective = None
        top_k_effective = top_k
        max_job_age_days_effective = max_age_days

    # Persist the uploaded file to a temporary path on disk for PyMuPDF
    tmp_dir = Path("tmp_uploads")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    resume_path = tmp_dir / uploaded_file.name
    resume_path.write_bytes(uploaded_file.read())

    with st.spinner("Running LinkedIn AI Agent..."):
        try:
            results = run_linkedin_agent_workflow(
                settings=settings,
                resume_path=str(resume_path),
                job_query=job_query_effective,
                location=location_effective,
                num_jobs=num_jobs_effective,
                top_k=top_k_effective,
                max_job_age_days=max_job_age_days_effective,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Error while running agent from UI")
            st.error(f"Error while running agent: {exc}")
            return

    if not results:
        st.warning("No results returned.")
        return

    st.subheader("Top Matching Jobs and Suggestions")

    for job in results:
        with st.expander(
            f"{job['title']} at {job['company']} "
            f"(Score: {job['score']}%, Location: {job['location']})",
            expanded=True,
        ):
            st.markdown(f"**Link:** [{job['link']}]({job['link']})")
            st.markdown(f"**Date:** {job.get('date', 'N/A')}")

            st.markdown("#### Improvement Suggestions")
            st.markdown(job["suggestions"])


if __name__ == "__main__":
    main()

