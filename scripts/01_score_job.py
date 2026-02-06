#!/usr/bin/env python3
"""
scripts/01_score_job.py

CLI to score a job posting against master profile using Grok.
Creates job folder under data/jobs/00001_xxxxxxxx style.

Now also extracts Company_website, Location, etc. from the top of the markdown file.

Usage:
    python scripts/01_score_job.py path/to/intake/job_file.md [--model grok-3] [--temperature 0.5] [--no-move]
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import yaml
from src.ai.grok_client import GrokClient
from src.loaders.master_profile import MasterProfileLoader

JOB_ROOT = Path("data/jobs")
INTAKE_ROOT = Path("intake")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score job against master profile.")
    parser.add_argument("job_file", type=Path, help="Path to intake markdown file")
    parser.add_argument("--model", default="grok-3", help="Grok model")
    parser.add_argument("--temperature", type=float, default=0.5, help="LLM temperature")
    parser.add_argument("--no-move", action="store_true", help="Don't move file from intake/")
    return parser.parse_args()


def extract_job_text(job_path: Path) -> str:
    if not job_path.is_file():
        raise FileNotFoundError(f"Job file not found: {job_path}")
    return job_path.read_text(encoding="utf-8")


def extract_front_matter(job_text: str) -> Dict[str, str]:
    """
    Extract key-value pairs from the top of the file (before the main content).
    Looks for lines like: Company_website: https://...
    Stops when it hits a line that doesn't look like metadata.
    """
    data: Dict[str, str] = {}
    lines = job_text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('---'):
            continue
        if ':' not in line:
            break  # stop at first non-metadata line
        key, value = line.split(':', 1)
        key = key.strip().lower().replace(' ', '_').replace('-', '_')
        value = value.strip()
        if value:
            data[key] = value
    return data


def extract_metadata_from_filename(filename: str) -> Dict[str, str]:
    """Parse from filename like 00002.PostScript.02052026.2243.md"""
    stem = Path(filename).stem
    parts = stem.split(".")
    if len(parts) < 3:
        return {"company": "Unknown", "role": "Unknown"}

    # num = parts[0]
    company = parts[1].replace("_", " ").title()

    # Role is everything after company until date-like part (8+ digits)
    rest_parts = parts[2:]
    role_parts = []
    for part in rest_parts:
        if re.match(r"^\d{8,}", part):  # Date like 02052026
            break
        role_parts.append(part.replace("_", " "))

    role = " ".join(role_parts).title().strip()
    if not role:
        role = "Unknown Role"

    return {"company": company, "role": role}


def get_next_job_number() -> int:
    """Find the highest existing 5-digit number in folders like 00001_xxxxxxxx"""
    pattern = re.compile(r"^(\d{5})_[0-9a-f]{8}$")
    numbers: List[int] = []

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
                "You are an expert career coach. Compare job to candidate profile. "
                "Give realistic 0-100 score, recommendation, strengths, gaps, advice. "
                "Be concise, quantitative, honest."
            ),
        },
        {
            "role": "user",
            "content": f"""\
Candidate profile summary:
{profile_summary}

Top skills:
{top_skills_str}

Recent experience:
{recent_experience_str}

Job:
{job_text}

Output EXACTLY this markdown:
## Match Score: X%
## Recommendation: Strong Proceed / Proceed / Hold / Skip
## Strongest Matches
- ...
## Gaps & Risks
- ... *Mitigation*: ...
## Advice
...
""",
        },
    ]


def parse_score_from_response(response: str) -> tuple[int, str]:
    score_match = re.search(r"## Match Score:\s*(\d+)%", response, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else 0
    rec_match = re.search(r"## Recommendation:\s*(.+?)(?=\n##|$)", response, re.IGNORECASE | re.DOTALL)
    rec = rec_match.group(1).strip() if rec_match else "Unknown"
    return score, rec


def create_job_folder(
    job_uuid: str,
    job_file: Path,
    job_text: str,               # ← added so we can extract front matter
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

    # Extract metadata
    meta_from_file = extract_metadata_from_filename(job_file.name)
    front_matter = extract_front_matter(job_text)

    # Prefer front-matter → fallback to filename
    company = front_matter.get("company_name", front_matter.get("company", meta_from_file["company"]))
    role = front_matter.get("title", front_matter.get("job_title", meta_from_file["role"]))

    # Move or copy original intake file
    target_original = job_dir / job_file.name
    if no_move:
        shutil.copy2(job_file, target_original)
        print(f"Copied (no-move): {job_file.name} → {target_original}")
    else:
        job_file.replace(target_original)
        print(f"Moved: {job_file.name} → {target_original}")

    # Standardized raw file
    raw_path = job_dir / "raw" / "raw_intake.md"
    shutil.copy2(target_original, raw_path)
    print(f"Created standardized raw: {raw_path}")

    # Score report
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = job_dir / "score" / f"score_report_{ts}.md"
    report_path.write_text(
        f"# Score Report for {job_file.stem}\n\n{score_response}", encoding="utf-8"
    )
    print(f"Saved score report: {report_path}")

    # metadata.yaml – now includes website & location
    metadata: Dict[str, Any] = {
        "uuid": job_uuid,
        "job_id": job_id,
        "original_filename": job_file.name,
        "company": company,
        "role": role,
        "company_website": front_matter.get("company_website", ""),
        "location": front_matter.get("location", "Unknown"),
        "status": "PENDING",
        "score": score,
        "recommendation": recommendation,
        "score_date": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
        "notes": f"Plano, TX location match. Score: {score}%. Recommendation: {recommendation}",
        "location_preference": "Plano, TX",
    }
    meta_path = job_dir / "metadata.yaml"
    with meta_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(metadata, f, sort_keys=False, allow_unicode=True)

    print(f"Created metadata: {meta_path}")
    print(f"  Company: {company}")
    print(f"  Website: {metadata['company_website'] or 'Not found'}")
    print(f"  Location: {metadata['location']}")

    print(f"✓ Job folder created: {job_dir}")
    print(f"  Structure: {job_file.name}, raw/raw_intake.md, score/score_report_*.md, metadata.yaml")
    return job_dir


def main() -> None:
    args = parse_arguments()

    if not args.job_file.exists():
        print(f"❌ Error: {args.job_file} does not exist.")
        sys.exit(1)

    print(f"🎯 Scoring job: {args.job_file.name}")

    # Load master profile
    try:
        print("📊 Loading master profile...")
        loader = MasterProfileLoader()
        profile_summary = loader.get_summary("short")
        top_skills = loader.get_top_skills(n=15)
        top_skills_str = "\n".join(
            f"- {s['name']} ({s.get('years', 'N/A')} yrs, {s.get('proficiency', 'N/A')})"
            for s in top_skills
        )
        recent_exp = loader.get_recent_experience(n=3)
        recent_experience_str = "\n".join(
            f"- {r.get('role')} at {r.get('company')} ({r.get('start')}–{r.get('end')})"
            for r in recent_exp
        )
        print("✅ Master profile loaded")
    except Exception as e:
        print(f"❌ Master profile load failed: {e}")
        sys.exit(1)

    # Read full job text (we need it for front-matter too)
    job_text = extract_job_text(args.job_file)
    print("📄 Job text extracted")

    # Score with Grok
    messages = build_scoring_prompt(
        job_text, profile_summary, top_skills_str, recent_experience_str
    )
    grok = GrokClient(model=args.model)
    try:
        print("🤖 Calling Grok for scoring...")
        response = grok.chat(
            messages=messages, temperature=args.temperature, max_tokens=1200
        )
        print("✅ Grok responded")
    except Exception as e:
        print(f"❌ Grok call failed: {e}")
        sys.exit(1)

    # Show results
    print("\n" + "=" * 80)
    print("🎯 GROK SCORE REPORT")
    print("=" * 80)
    print(response)
    print("=" * 80)

    score, recommendation = parse_score_from_response(response)
    print(f"📈 Parsed: Score={score}%, Recommendation={recommendation}")

    # Create structured job folder
    job_uuid = str(uuid.uuid4())
    job_dir = create_job_folder(
        job_uuid=job_uuid,
        job_file=args.job_file,
        job_text=job_text,           # ← passed here
        score_response=response,
        score=score,
        recommendation=recommendation,
        no_move=args.no_move,
    )

    print(f"\n✅ SUCCESS")
    print(f"📁 Job folder: {job_dir}")
    print(f"🆔 Job UUID: {job_uuid}")
    print(f"📊 Status: PENDING (score_report in score/ folder)")
    print("\n🚀 Next steps:")
    print(f"1. Review {job_dir}/score/score_report_*.md")
    print(f"2. If good → python scripts/02_accept_job.py --uuid {job_uuid}")
    print(f"3. Then tailor → python scripts/03_tailor_job_data.py --uuid {job_uuid}")


if __name__ == "__main__":
    main()