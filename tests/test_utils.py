from __future__ import annotations

from linkedin_agent.agent import _job_age_in_days
from linkedin_agent.memory import JSONMemoryStore


def test_job_age_in_days_basic() -> None:
    assert _job_age_in_days("Today") == 0
    assert _job_age_in_days("Yesterday") == 1
    assert _job_age_in_days("3 days ago") == 3
    # Unknown formats should return None rather than throwing.
    assert _job_age_in_days("sometime last year") is None


def test_json_memory_store_roundtrip(tmp_path) -> None:
    path = tmp_path / "test_memory.json"
    store = JSONMemoryStore(path)

    profile_id = "test-profile"
    job_link = "https://example.com/job/123"
    job_title = "AI Engineer"
    company = "Example Corp"

    store.add_interaction(
        profile_id=profile_id,
        job_link=job_link,
        job_title=job_title,
        company=company,
        score=95.0,
        suggestions="Do more with LLMs.",
    )

    interactions = store.get_interactions(profile_id)
    assert len(interactions) == 1
    record = interactions[0]
    assert record.job_link == job_link
    assert record.job_title == job_title
    assert record.company == company
    assert record.score == 95.0

