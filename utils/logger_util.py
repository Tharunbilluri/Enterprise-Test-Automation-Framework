"""Structured logging utility with console and timestamped file handlers."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from config.settings import get_settings
from utils.file_util import ensure_directory, timestamp_slug


_LOGGER_NAME = "enterprise_taf"
_configured = False


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return a configured logger.

    The root framework logger is initialized once with:
    - Console handler (stdout)
    - File handler under ``logs/`` with a timestamped filename
    """
    global _configured

    settings = get_settings()
    logger = logging.getLogger(name or _LOGGER_NAME)

    if not _configured:
        logger.setLevel(getattr(logging, settings.log_level, logging.INFO))
        logger.handlers.clear()
        logger.propagate = False

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logger.level)
        console.setFormatter(formatter)
        logger.addHandler(console)

        log_dir = ensure_directory(settings.logs_dir)
        log_file = log_dir / f"test_run_{timestamp_slug()}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logger.level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        _configured = True
        logger.debug("Logging initialized. File=%s", log_file)

    if name and name != _LOGGER_NAME:
        child = logging.getLogger(name)
        child.setLevel(logger.level)
        return child

    return logger


def reset_logger_for_tests() -> None:
    """Reset logger configuration (useful in unit tests of the framework)."""
    global _configured
    root = logging.getLogger(_LOGGER_NAME)
    for handler in list(root.handlers):
        handler.close()
        root.removeHandler(handler)
    _configured = False
