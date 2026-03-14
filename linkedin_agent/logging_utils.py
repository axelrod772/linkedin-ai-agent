from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "agent.log"


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure application-wide logging with a rotating file handler.

    All agent thoughts, actions, and high-level events should log via the
    root logger or the ``linkedin_agent`` logger so they end up in
    ``logs/agent.log``.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    if any(isinstance(h, RotatingFileHandler) and getattr(h, "_agent_log", False) for h in logger.handlers):
        # Already configured in this process.
        return

    logger.setLevel(level)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )
    # Sentinel attribute so we do not attach multiple times.
    file_handler._agent_log = True  # type: ignore[attr-defined]

    logger.addHandler(file_handler)

