from __future__ import annotations

from pathlib import Path
import logging
from typing import Optional

import streamlit as st

from linkedin_agent import run_linkedin_agent_workflow
from linkedin_agent.config import load_settings
from linkedin_agent.logging_utils import configure_logging


def main() -> None:
    configure_logging()
    logger = logging.getLogger("linkedin_agent.ui")

    st.set_page_config(page_title="LinkedIn AI Agent", layout="wide")
    st.title("LinkedIn AI Agent – Resume & Job Match")
    st.markdown(
        "Upload your resume, choose a target role, and the agent will "
        "analyze realistic AI/ML job descriptions to suggest concrete improvements."
    )

    with st.sidebar:
        st.header("Configuration")
        query_default = "AI Engineer"
        job_query = st.text_input("Target role / query", value=query_default)
        location = st.text_input("Location", value="Remote")
        top_k = st.slider("Top matching jobs", min_value=1, max_value=5, value=3)

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    run_button_disabled = uploaded_file is None or not job_query.strip()
    run_clicked = st.button("Run analysis", type="primary", disabled=run_button_disabled)

    if run_button_disabled:
        st.info("Upload a PDF resume and enter a query to begin.")

    if not run_clicked:
        return

    if uploaded_file is None:
        st.error("Please upload a resume PDF.")
        return

    settings = load_settings()

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
                job_query=job_query,
                location=location,
                num_jobs=None,
                top_k=top_k,
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

