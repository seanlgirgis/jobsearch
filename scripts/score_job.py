# scripts/score_job.py
"""
CLI script to score a job posting against your master profile using Grok.

Usage:
    python -m scripts.score_job path/to/intake/job_file.md

Outputs:
    - Console report
    - Saves score_report.md next to the input file
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from src.ai.grok_client import GrokClient
from src.loaders.master_profile import MasterProfileLoader


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score a job posting against your profile.")
    parser.add_argument(
        "job_file",
        type=Path,
        help="Path to the job intake markdown file (e.g. intake/00001....md)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="grok-3",
        help="Grok model to use (default: grok-3)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.5,
        help="Temperature for LLM generation (default: 0.5)",
    )
    return parser.parse_args()


def extract_job_text(job_path: Path) -> str:
    """Read and clean the job markdown file content."""
    if not job_path.is_file():
        raise FileNotFoundError(f"Job file not found: {job_path}")
    text = job_path.read_text(encoding="utf-8")
    # Basic cleaning – remove excessive whitespace, keep structure
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def build_scoring_prompt(
    job_text: str,
    profile_summary: str,
    top_skills_str: str,
    recent_experience_str: str,
) -> list[dict[str, str]]:
    """Construct the prompt for Grok to score the job match."""
    return [
        {
            "role": "system",
            "content": (
                "You are an expert career coach and resume optimizer. "
                "Your task is to compare a job description to a candidate's master profile "
                "and give a realistic match score (0–100), recommendation, strengths, gaps, "
                "and specific advice. Be honest, quantitative where possible, and concise."
            ),
        },
        {
            "role": "user",
            "content": f"""\
Here is the candidate's master profile summary:
{profile_summary}

Top skills with years and proficiency:
{top_skills_str}

Most recent experience (last 2–3 roles):
{recent_experience_str}

Job description to evaluate:
{job_text}

Tasks:
1. Calculate an overall match score (0–100) based on:
   - Skill overlap (years, proficiency, keywords)
   - Experience relevance (years, domain, scale)
   - Leadership / soft requirements
   - Domain knowledge (healthcare is a plus here)
2. Recommend: Strong Proceed / Proceed with Prep / Borderline / Skip
3. List 4–6 strongest matches (with evidence)
4. List 3–5 biggest gaps or risks (with mitigation ideas)
5. Overall advice (1–2 sentences)

Output format (markdown):
## Match Score: XX%
## Recommendation: ...
## Strongest Matches
- ...
## Gaps & Risks
- ...
## Advice
...
""",
        },
    ]

# ... (keep everything above main() the same)

def create_job_folder(uuid: str, job_file: Path, report_content: str) -> Path:
    """Create job tracking folder and save initial files."""
    job_dir = Path("data/jobs") / uuid
    job_dir.mkdir(parents=True, exist_ok=True)

    # Copy raw intake
    intake_dest = job_dir / "raw_intake.md"
    job_file.replace(intake_dest)  # move original to job folder (or .copy() if you want to keep original)

    # Save score report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = job_dir / f"score_report_{timestamp}.md"
    report_path.write_text(report_content, encoding="utf-8")

    # Create metadata.yaml
    metadata = {
        "uuid": uuid,
        "title": job_file.stem,  # or parse from content later
        "company": "Collective Health",  # improve parsing later
        "role": "Staff Data Engineer",
        "status": "PENDING",
        "score": 85,  # parse from response or hardcode for v0.2
        "score_date": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
        "notes": ""
    }
    metadata_path = job_dir / "metadata.yaml"
    with metadata_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(metadata, f, sort_keys=False)

    print(f"Job folder created: {job_dir}")
    print(f"Files: raw_intake.md, score_report_..., metadata.yaml")
    return job_dir


def main() -> None:
    args = parse_arguments()

    print(f"Scoring job: {args.job_file.name}")

    # ... (keep loading profile, job_text, grok call the same)

    # After successful grok response
    print("\n" + "=" * 60)
    print("SCORE REPORT")
    print("=" * 60)
    print(response)

    # Auto-create job tracking
    import uuid
    job_uuid = str(uuid.uuid4())
    create_job_folder(job_uuid, args.job_file, response)

    print(f"\nJob UUID: {job_uuid}")
    print("Status: PENDING – run accept_job.py or reject_job.py next")