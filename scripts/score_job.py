#!/usr/bin/env python3
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
import os   # ← add this
import shutil  # needed if you use shutil.copy instead of .replace()
import yaml 
from src.ai.grok_client import GrokClient
from src.loaders.master_profile import MasterProfileLoader

JOB_ROOT = Path("data/jobs")  # ← Add this here (missing global)

print("Script started - imports passed")
print("Current dir:", Path.cwd())
print("PYTHONPATH:", os.environ.get("PYTHONPATH", "not set"))

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
1. Score overall match (0-100) based on skills, experience, and requirements.
2. Recommendation: Strong Proceed, Proceed, Hold, or Skip. Explain briefly.
3. Strongest Matches: 5-7 bullet points of key alignments (skills, exp, etc.).
4. Gaps & Risks: 3-5 bullet points of mismatches or concerns, with mitigation advice.
5. Advice: 1-2 sentences on next steps (apply? tailor resume? upskill?).

Output EXACTLY in this markdown format:
## Match Score: X%
## Recommendation: Y
## Strongest Matches
- Bullet 1
- Bullet 2
## Gaps & Risks
- Bullet 1 *Mitigation*: Advice
- Bullet 2 *Mitigation*: Advice
## Advice
Short paragraph.
""",
        },
    ]


def create_job_folder(uuid_str: str, job_file: Path, score_response: str) -> Path:
    job_dir = JOB_ROOT / uuid_str
    job_dir.mkdir(parents=True, exist_ok=True)

    # MOVE original file to job folder (removes from intake/)
    original_name_in_job = job_dir / job_file.name
    shutil.move(str(job_file), str(original_name_in_job))  # ← move instead of copy

    # Also create raw_intake.md copy for script compatibility
    raw_intake_path = job_dir / "raw_intake.md"
    shutil.copy(str(original_name_in_job), str(raw_intake_path))

    # Save score report with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = job_dir / f"score_report_{timestamp}.md"
    report_content = f"# Score Report for {job_file.stem}\n\n{score_response}"
    report_path.write_text(report_content, encoding="utf-8")

    # Create/update metadata.yaml
    metadata = {
        "uuid": uuid_str,
        "original_filename": job_file.name,
        "title": job_file.stem,  # fallback
        "company": "Collective Health",  # TODO: parse from filename or content
        "role": "Staff Data Engineer",
        "status": "PENDING",
        "score": 85,  # TODO: parse real score from response
        "score_date": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
        "notes": ""
    }
    metadata_path = job_dir / "metadata.yaml"
    with metadata_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(metadata, f, sort_keys=False)

    print(f"Job folder created: {job_dir}")
    print(f"Files: {original_name_in_job.name} (moved from intake), raw_intake.md, score_report_..., metadata.yaml")
    return job_dir


def main() -> None:
    args = parse_arguments()

    print(f"Scoring job: {args.job_file.name}")

    # Debug prints
    print("Script started - imports passed")
    print("Current dir:", Path.cwd())
    print("PYTHONPATH:", os.environ.get("PYTHONPATH", "not set"))

    # Load master profile
    try:
        loader = MasterProfileLoader()
        print("Master profile loaded successfully")
    except Exception as e:
        print("Error loading master profile:")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    profile_summary = loader.get_summary("short")
    top_skills = loader.get_top_skills(n=15)
    top_skills_str = "\n".join(
        f"- {s['name']} ({s.get('years')} yrs, {s.get('proficiency', 'N/A')})"
        for s in top_skills
    )
    recent_exp = loader.get_recent_experience(n=3)
    recent_experience_str = "\n".join(
        f"- {r.get('role')} at {r.get('company')} ({r.get('start')} – {r.get('end')})"
        for r in recent_exp
    )

    # Load job text
    try:
        job_text = extract_job_text(args.job_file)
        print("Job description loaded")
    except Exception as e:
        print(f"Error reading job file: {e}")
        sys.exit(1)

    # Build prompt and call Grok
    messages = build_scoring_prompt(
        job_text=job_text,
        profile_summary=profile_summary,
        top_skills_str=top_skills_str,
        recent_experience_str=recent_experience_str,
    )

    grok = GrokClient(model=args.model)
    try:
        print("Calling Grok for scoring...")
        response = grok.chat(
            messages=messages,
            temperature=args.temperature,
            max_tokens=1200,
        )
        print("Grok responded successfully")
    except Exception as e:
        print("Grok API call failed:")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Print report
    print("\n" + "=" * 60)
    print("SCORE REPORT")
    print("=" * 60)
    print(response)

    # Auto-create job folder and UUID
    import uuid
    job_uuid = str(uuid.uuid4())
    create_job_folder(job_uuid, args.job_file, response)

    print(f"\nJob UUID: {job_uuid}")
    print("Status: PENDING — next step: accept, reject, or tailor")

if __name__ == "__main__":
    main()