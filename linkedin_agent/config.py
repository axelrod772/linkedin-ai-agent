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
    )

