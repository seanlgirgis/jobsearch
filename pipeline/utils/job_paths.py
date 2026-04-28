"""Helpers for creating job IDs and job folder paths."""

import re
import uuid
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
JOBS_ROOT = PROJECT_ROOT / "data" / "jobs"
JOB_ID_PATTERN = re.compile(r"^(\d{5})_[0-9a-f]{8}$")


def get_next_job_number() -> int:
    """Return next incremental 5-digit job number."""
    numbers: list[int] = []

    if not JOBS_ROOT.exists():
        return 1

    for child in JOBS_ROOT.iterdir():
        if not child.is_dir():
            continue
        match = JOB_ID_PATTERN.match(child.name)
        if match:
            numbers.append(int(match.group(1)))

    return max(numbers) + 1 if numbers else 1


def create_job_id() -> str:
    """Create job ID like 00001_ab12cd34."""
    next_number = get_next_job_number()
    short_uuid = str(uuid.uuid4())[:8]
    return f"{next_number:05d}_{short_uuid}"


def create_job_folder(job_id: str) -> Path:
    """Create standard pipeline job folders and return the job directory path."""
    job_dir = JOBS_ROOT / job_id
    for subdir in ("raw", "score", "tailored", "generated", "research"):
        (job_dir / subdir).mkdir(parents=True, exist_ok=True)
    return job_dir

