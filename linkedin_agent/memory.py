from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class InteractionRecord:
    profile_id: str
    job_link: str
    job_title: str
    company: str
    score: float
    suggestions: str
    created_at: str


class JSONMemoryStore:
    """
    Simple JSON-based persistent memory.

    The goal is to keep track of previous interactions with
    specific profiles and jobs so the agent can reuse or
    reference past suggestions.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._data: Dict[str, List[InteractionRecord]] = {}
        self._load()

    @staticmethod
    def profile_id_from_resume(resume_text: str) -> str:
        """
        Stable identifier for a resume based on its contents.
        """
        digest = hashlib.sha256(resume_text.encode("utf-8")).hexdigest()
        return digest

    def _load(self) -> None:
        if not self.path.exists():
            self._data = {}
            return

        with self.path.open("r", encoding="utf-8") as f:
            raw = json.load(f)

        self._data = {
            profile_id: [
                InteractionRecord(**record) for record in records  # type: ignore[arg-type]
            ]
            for profile_id, records in raw.items()
        }

    def _save(self) -> None:
        serializable: Dict[str, List[Dict[str, Any]]] = {
            profile_id: [asdict(record) for record in records]
            for profile_id, records in self._data.items()
        }

        with self.path.open("w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)

    # Public API used by the agent and tools

    def get_interactions(self, profile_id: str) -> List[InteractionRecord]:
        """
        Return all previous interactions for a given profile id.
        """
        return list(self._data.get(profile_id, []))

    def add_interaction(
        self,
        profile_id: str,
        job_link: str,
        job_title: str,
        company: str,
        score: float,
        suggestions: str,
    ) -> InteractionRecord:
        record = InteractionRecord(
            profile_id=profile_id,
            job_link=job_link,
            job_title=job_title,
            company=company,
            score=score,
            suggestions=suggestions,
            created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )

        if profile_id not in self._data:
            self._data[profile_id] = []

        self._data[profile_id].append(record)
        self._save()
        return record

