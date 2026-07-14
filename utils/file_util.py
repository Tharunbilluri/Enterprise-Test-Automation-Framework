"""Filesystem helpers for testdata, artifacts, and timestamps."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def timestamp_slug(moment: datetime | None = None) -> str:
    """Return a filesystem-safe UTC timestamp, e.g. ``20260714_070512``."""
    current = moment or datetime.now(timezone.utc)
    return current.strftime("%Y%m%d_%H%M%S")


def ensure_directory(path: Path | str) -> Path:
    """Create ``path`` (and parents) if missing; return as ``Path``."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def sanitize_filename(value: str, max_length: int = 120) -> str:
    """Strip characters that are unsafe in file names."""
    cleaned = re.sub(r"[^\w.\-]+", "_", value.strip())
    cleaned = cleaned.strip("._") or "artifact"
    return cleaned[:max_length]


def read_json(path: Path | str) -> Any:
    """Load and return JSON content from ``path``."""
    file_path = Path(path)
    with file_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path | str, data: Any, *, indent: int = 2) -> Path:
    """Write ``data`` as JSON; create parent directories as needed."""
    file_path = Path(path)
    ensure_directory(file_path.parent)
    with file_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=indent)
        handle.write("\n")
    return file_path


def resolve_testdata_path(relative_name: str, base: Path | None = None) -> Path:
    """
    Resolve a testdata file path relative to ``testdata/``.

    Example: ``resolve_testdata_path("login_credentials.json")``
    """
    from config.paths import TESTDATA_DIR

    root = base or TESTDATA_DIR
    candidate = root / relative_name
    if not candidate.is_file():
        raise FileNotFoundError(f"Testdata file not found: {candidate}")
    return candidate


def load_testdata(relative_name: str) -> Any:
    """Read JSON testdata by relative file name under ``testdata/``."""
    return read_json(resolve_testdata_path(relative_name))
