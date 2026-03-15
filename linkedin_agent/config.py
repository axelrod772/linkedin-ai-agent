import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Settings:
    """
    Central configuration for the LinkedIn agent.

    Values are loaded from environment variables so that
    secrets and deployment-specific settings stay outside code.
    """

    # LLM configuration
    openai_api_key: str | None
    openai_model_name: str

    # Optional NVIDIA model support (not required for core flow)
    nvidia_api_key: str | None
    nvidia_model_name: str

    # Application configuration
    default_location: str
    default_num_jobs: int
    memory_path: str
    chroma_dir: str
    max_job_age_days: int
    default_experience_level: str
    page_timeout_seconds: int
    agent_default_top_k: int


def load_settings() -> Settings:
    """
    Load settings from `.env` and process environment.
    """
    load_dotenv()

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model_name=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"),
        nvidia_api_key=os.getenv("NVIDIA_API_KEY"),
        nvidia_model_name=os.getenv("NVIDIA_MODEL_NAME", "meta/llama-3.1-8b-instruct"),
        default_location=os.getenv("LINKEDIN_DEFAULT_LOCATION", "Remote"),
        default_num_jobs=int(os.getenv("LINKEDIN_DEFAULT_NUM_JOBS", "20")),
        memory_path=os.getenv("LINKEDIN_MEMORY_PATH", "linkedin_memory.json"),
        chroma_dir=os.getenv("LINKEDIN_CHROMA_DIR", "chroma_db"),
        max_job_age_days=int(os.getenv("LINKEDIN_MAX_JOB_AGE_DAYS", "3")),
        default_experience_level=os.getenv("LINKEDIN_DEFAULT_EXPERIENCE_LEVEL", "any"),
        page_timeout_seconds=int(os.getenv("LINKEDIN_PAGE_TIMEOUT_SECONDS", "60")),
        agent_default_top_k=int(os.getenv("AGENT_DEFAULT_TOP_K", "5")),
    )

