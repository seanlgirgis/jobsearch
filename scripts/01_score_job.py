#!/usr/bin/env python3
"""
scripts/01_score_job.py

CLI to score a job posting against master profile using Grok.
Creates job folder under data/jobs/00001_xxxxxxxx style.

Fixed/hardened version:
- Uses stricter scoring calibration aligned to Sean's target roles.
- Lowers default temperature for deterministic scoring.
- Adds recommendation normalization and score/recommendation consistency checks.
- Avoids hardcoded Plano notes.
- Preserves front-matter company/title/location/website extraction.
- Keeps markdown score_report output compatible with existing pipeline.

Usage:
    python scripts/01_score_job.py path/to/intake/job_file.md [--model grok-3] [--temperature 0.0] [--no-move]
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml

from src.ai.grok_client import GrokClient
from src.loaders.master_profile import MasterProfileLoader

JOB_ROOT = Path("data/jobs")
INTAKE_ROOT = Path("intake")

VALID_RECOMMENDATIONS = {
    "Strong Proceed",
    "Proceed",
    "Hold",
    "Skip",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score job against master profile.")
    parser.add_argument("job_file", type=Path, help="Path to intake markdown file")
    parser.add_argument("--model", default="grok-3", help="Grok model")
    parser.add_argument("--temperature", type=float, default=0.0, help="LLM temperature")
    parser.add_argument("--no-move", action="store_true", help="Don't move file from intake/")
    return parser.parse_args()


def extract_job_text(job_path: Path) -> str:
    if not job_path.is_file():
        raise FileNotFoundError(f"Job file not found: {job_path}")
    return job_path.read_text(encoding="utf-8")


def extract_front_matter(job_text: str) -> Dict[str, str]:
    """
    Extract key-value pairs from the top of the file.
    Looks for lines like:
      Company_Name: Example
      Company_website: https://example.com
      Title: Senior Data Engineer
      Location: Remote
    Stops when it hits the first non-metadata line.
    """
    data: Dict[str, str] = {}
    lines = job_text.splitlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("---"):
            continue
        if ":" not in line:
            break

        key, value = line.split(":", 1)
        key = key.strip().lower().replace(" ", "_").replace("-", "_")
        value = value.strip()

        if value:
            data[key] = value

    return data


def extract_metadata_from_filename(filename: str) -> Dict[str, str]:
    """Parse from filename like 00002.PostScript.Senior_Data_Engineer.02052026.md"""
    stem = Path(filename).stem
    parts = stem.split(".")

    if len(parts) < 2:
        return {"company": "", "role": ""}

    company = parts[1].replace("_", " ").title() if len(parts) > 1 else ""

    role_parts = []
    for part in parts[2:]:
        if re.match(r"^\d{6,}", part):
            break
        role_parts.append(part.replace("_", " "))

    role = " ".join(role_parts).title().strip()

    return {"company": company, "role": role}


def get_next_job_number() -> int:
    """Find highest existing 5-digit number in folders like 00001_xxxxxxxx."""
    pattern = re.compile(r"^(\d{5})_[0-9a-f]{8}$")
    numbers: List[int] = []

    if not JOB_ROOT.exists():
        JOB_ROOT.mkdir(parents=True, exist_ok=True)
        return 1

    for d in JOB_ROOT.iterdir():
        if d.is_dir():
            match = pattern.match(d.name)
            if match:
                numbers.append(int(match.group(1)))

    return max(numbers) + 1 if numbers else 1


def build_scoring_prompt(
    job_text: str,
    profile_summary: str,
    top_skills_str: str,
    recent_experience_str: str,
) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You are Sean's strict job-fit scoring engine for senior data engineering applications.\n"
                "Use only the supplied candidate profile summary, skills, recent experience, and job posting.\n"
                "Never invent candidate experience.\n"
                "Never be optimistic if the fit is weak.\n"
                "Return only the requested markdown headings.\n"
            ),
        },
        {
            "role": "user",
            "content": f"""Candidate profile summary:
{profile_summary}

Top skills:
{top_skills_str}

Recent experience:
{recent_experience_str}

Job posting:
{job_text}

SCORING FRAMEWORK:
- Core Stack Match (35%): AWS, Python, SQL, Spark/PySpark, ETL, data warehousing, data lakes.
- Role Alignment (20%): Prefer Senior Data Engineer, AWS Data Engineer, ML Data Engineer with light/applied ML.
- Experience Fit (15%): Candidate has 20+ years. Strong fit for senior/staff hands-on roles. Penalize junior roles and executive/director roles unless clearly hands-on.
- Domain Match (15%): Prefer pipelines, telemetry, forecasting, cloud data platforms, analytics engineering, data quality, orchestration.
- Risk Factors (-15%): Penalize deep-learning-heavy roles, pure ML research, TensorFlow/PyTorch as core, heavy Kafka production depth if required, robotics/biotech/research domain mismatch, junior overqualification.

SCORE CALIBRATION:
- 90-100: Exceptional fit; candidate can interview today with minimal repositioning.
- 85-89: Strong fit; only minor risks.
- 75-84: Solid fit; apply if aligned.
- 65-74: Borderline; hold unless strategic.
- Below 65: Skip.
- Missing hard must-have skills should reduce score.
- Do not give 85+ if the job is primarily deep learning, pure ML research, director/executive, or junior.

DECISION RULES:
- 85-100 -> Strong Proceed
- 75-84 -> Proceed
- 65-74 -> Hold
- <65 -> Skip

POSITIONING RULE:
Always recommend one dominant positioning angle, preferably one of:
- AWS Data Engineer specializing in ML-enabled pipelines and scalable data platforms
- Senior Data Engineer specializing in cloud data platforms
- Hands-on Senior Data Engineer
- ML Data Engineer (light ML only)

Avoid positioning as "ML Engineer" unless the job and candidate evidence justify it.
ML should usually be framed as forecasting, scikit-learn/Prophet, and ML-enabled data pipelines.

Output EXACTLY this markdown (no extra text):
## Match Score: X%
## Recommendation: Strong Proceed / Proceed / Hold / Skip
## Strongest Matches
- bullet per concrete match
## Gaps & Risks
- bullet per missing must-have or risk. Mitigation: one sentence fix.
## ATS Keywords Present
- list keywords from the job already supported by candidate profile
## ATS Keywords Missing
- list important job keywords not strongly supported by candidate profile
## Advice
2-4 concrete sentences. Include the recommended positioning angle explicitly.
""",
        },
    ]


def normalize_recommendation(raw: str, score: int) -> str:
    text = (raw or "").strip()

    for valid in VALID_RECOMMENDATIONS:
        if valid.lower() == text.lower():
            return valid

    if "strong" in text.lower() and "proceed" in text.lower():
        return "Strong Proceed"
    if "proceed" in text.lower() or "apply" in text.lower():
        return "Proceed"
    if "hold" in text.lower() or "conditional" in text.lower():
        return "Hold"
    if "skip" in text.lower() or "reject" in text.lower():
        return "Skip"

    if score >= 85:
        return "Strong Proceed"
    if score >= 75:
        return "Proceed"
    if score >= 65:
        return "Hold"
    return "Skip"


def enforce_recommendation_consistency(score: int, recommendation: str) -> str:
    expected = normalize_recommendation("", score)
    if recommendation != expected:
        print(
            f"Warning: recommendation '{recommendation}' inconsistent with score {score}; "
            f"normalizing to '{expected}'"
        )
        return expected
    return recommendation


def parse_score_from_response(response: str) -> tuple[int, str]:
    score_match = re.search(r"## Match Score:\s*(\d+)%", response, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else 0
    score = max(0, min(100, score))

    rec_match = re.search(
        r"## Recommendation:\s*(.+?)(?=\n##|$)",
        response,
        re.IGNORECASE | re.DOTALL,
    )
    raw_rec = rec_match.group(1).strip() if rec_match else ""
    recommendation = normalize_recommendation(raw_rec, score)
    recommendation = enforce_recommendation_consistency(score, recommendation)

    return score, recommendation


def create_job_folder(
    job_uuid: str,
    job_file: Path,
    job_text: str,
    score_response: str,
    score: int,
    recommendation: str,
    no_move: bool = False,
) -> Path:
    next_num = get_next_job_number()
    short_uuid = job_uuid[:8]
    job_id = f"{next_num:05d}_{short_uuid}"

    job_dir = JOB_ROOT / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    (job_dir / "raw").mkdir(exist_ok=True)
    (job_dir / "score").mkdir(exist_ok=True)

    meta_from_file = extract_metadata_from_filename(job_file.name)
    front_matter = extract_front_matter(job_text)

    company = (
        front_matter.get("company_name")
        or front_matter.get("company")
        or front_matter.get("employer_name")
        or meta_from_file.get("company", "")
    )
    role = (
        front_matter.get("title")
        or front_matter.get("job_title")
        or front_matter.get("role")
        or meta_from_file.get("role", "")
    )
    company_website = (
        front_matter.get("company_website")
        or front_matter.get("website")
        or front_matter.get("url")
        or ""
    )
    location = front_matter.get("location", "")

    target_original = job_dir / job_file.name
    if no_move:
        shutil.copy2(job_file, target_original)
        print(f"Copied (no-move): {job_file.name} → {target_original}")
    else:
        job_file.replace(target_original)
        print(f"Moved: {job_file.name} → {target_original}")

    raw_path = job_dir / "raw" / "raw_intake.md"
    shutil.copy2(target_original, raw_path)
    print(f"Created standardized raw: {raw_path}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = job_dir / "score" / f"score_report_{ts}.md"
    report_path.write_text(
        f"# Score Report for {job_file.stem}\n\n{score_response}",
        encoding="utf-8",
    )
    print(f"Saved score report: {report_path}")

    metadata: Dict[str, Any] = {
        "uuid": job_uuid,
        "job_id": job_id,
        "original_filename": job_file.name,
        "company": company,
        "role": role,
        "company_website": company_website,
        "location": location,
        "status": "PENDING",
        "score": score,
        "recommendation": recommendation,
        "score_date": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
        "notes": f"Score: {score}%. Recommendation: {recommendation}",
    }

    meta_path = job_dir / "metadata.yaml"
    with meta_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(metadata, f, sort_keys=False, allow_unicode=True)

    print(f"Created metadata: {meta_path}")
    print(f"  Company: {company or '(empty)'}")
    print(f"  Website: {company_website or '(empty)'}")
    print(f"  Location: {location or '(empty)'}")
    print(f"✓ Job folder created: {job_dir}")
    return job_dir


def main() -> None:
    args = parse_arguments()

    if not args.job_file.exists():
        print(f"Error: {args.job_file} does not exist.")
        sys.exit(1)

    print(f"Scoring job: {args.job_file.name}")

    try:
        print("Loading master profile...")
        loader = MasterProfileLoader()
        profile_summary = loader.get_summary("short")
        top_skills = loader.get_top_skills(n=25)
        top_skills_str = "\n".join(
            f"- {s['name']} ({s.get('years', '')} yrs, {s.get('proficiency', '')})"
            for s in top_skills
        )
        recent_exp = loader.get_recent_experience(n=4)
        recent_experience_str = "\n".join(
            f"- {r.get('role')} at {r.get('company')} ({r.get('start')}–{r.get('end')})"
            for r in recent_exp
        )
        print("Master profile loaded")
    except Exception as exc:
        print(f"Master profile load failed: {exc}")
        sys.exit(1)

    job_text = extract_job_text(args.job_file)
    print("Job text extracted")

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
            max_tokens=1600,
        )
        print("Grok responded")
    except Exception as exc:
        print(f"Grok call failed: {exc}")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("SCORE REPORT")
    print("=" * 80)
    print(response)
    print("=" * 80)

    score, recommendation = parse_score_from_response(response)
    print(f"Parsed: Score={score}%, Recommendation={recommendation}")

    job_uuid = str(uuid.uuid4())
    job_dir = create_job_folder(
        job_uuid=job_uuid,
        job_file=args.job_file,
        job_text=job_text,
        score_response=response,
        score=score,
        recommendation=recommendation,
        no_move=args.no_move,
    )

    print("\nSUCCESS")
    print(f"Job folder: {job_dir}")
    print(f"Job UUID: {job_uuid}")
    print("Status: PENDING")
    print("\nNext steps:")
    print(f"1. Review {job_dir}/score/score_report_*.md")
    print(f"2. If good → python scripts/02_accept_job.py --uuid {job_uuid}")
    print(f"3. Then tailor → python scripts/03_tailor_job_data.py --uuid {job_uuid}")


if __name__ == "__main__":
    main()
