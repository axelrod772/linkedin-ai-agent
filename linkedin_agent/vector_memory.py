from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from .config import Settings


def get_vector_store(settings: Settings) -> Chroma:
    """
    Create (or load) a persistent ChromaDB vector store for profile memory.
    """
    persist_dir = Path(settings.chroma_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)

    embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
    return Chroma(
        collection_name="linkedin_profiles",
        embedding_function=embeddings,
        persist_directory=str(persist_dir),
    )


def add_profile_document(
    vector_store: Chroma,
    text: str,
    metadata: Dict[str, Any],
    doc_id: str | None = None,
) -> None:
    """
    Add a single profile document (lead, job, or person) to the vector store.
    """
    vector_store.add_texts(
        texts=[text],
        metadatas=[metadata],
        ids=[doc_id] if doc_id is not None else None,
    )
    vector_store.persist()


def find_similar_profiles(
    vector_store: Chroma,
    query_text: str,
    k: int = 3,
) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Retrieve the top-k most similar stored profiles for the given text.

    Returns a list of (text, metadata) tuples.
    """
    results = vector_store.similarity_search(query_text, k=k)
    return [(doc.page_content, doc.metadata or {}) for doc in results]

