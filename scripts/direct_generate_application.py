#!/usr/bin/env python3
"""
scripts/direct_generate_application.py

Lean "direct mode" generator:
- No scoring/decision/FAISS steps
- Uses master datastore + job text directly
- Produces tailored resume + cover artifacts in one command

Usage:
    python scripts/direct_generate_application.py --job 00051_5ade9538
    python scripts/direct_generate_application.py --job 5ade9538 --version direct-v2
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ai.grok_client import GrokClient

JOB_ROOT = Path("data/jobs")
DATA_ROOT = Path("data")
MASTER_ROOT = Path("data/master")


def resolve_job_folder(job_ref: str) -> Path:
    ref = job_ref.strip()
    exact = JOB_ROOT / ref
    if exact.is_dir():
        return exact

    candidates = list(JOB_ROOT.glob(f"*_{ref}*"))
    if not candidates and len(ref) >= 8:
        candidates = list(JOB_ROOT.glob(f"*_{ref[:8]}*"))

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        joined = ", ".join(c.name for c in candidates)
        raise ValueError(f"Ambiguous job reference '{job_ref}'. Matches: {joined}")

    raise ValueError(f"Job folder not found for '{job_ref}'")


def load_master_datastore() -> dict[str, Any]:
    source_of_truth_path = DATA_ROOT / "source_of_truth.json"
    if source_of_truth_path.is_file():
        with source_of_truth_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    master_json_path = MASTER_ROOT / "master_career_data.json"
    skills_yaml_path = MASTER_ROOT / "skills.yaml"
    if not master_json_path.is_file():
        raise FileNotFoundError("Missing master datastore: data/source_of_truth.json or data/master/master_career_data.json")

    with master_json_path.open("r", encoding="utf-8") as f:
        master = json.load(f)
    if skills_yaml_path.is_file():
        with skills_yaml_path.open("r", encoding="utf-8") as f:
            master["skills"] = yaml.safe_load(f) or []
    return master


def load_job_text(job_folder: Path) -> str:
    candidate_paths = [
        job_folder / "raw" / "raw_intake.md",
        job_folder / "intake.md",
        job_folder / "raw_intake.md",
    ]
    for path in candidate_paths:
        if path.is_file():
            return path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"No intake text found under {job_folder}")


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return json.loads(fenced.group(1))

    raw = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if raw:
        return json.loads(raw.group(0))

    raise ValueError("Could not parse JSON from LLM response")


def build_resume_prompt(master: dict[str, Any], job_text: str) -> str:
    return f"""
You are a strict resume generator. Output ONLY valid JSON, no markdown.

Rules:
1. Use only facts from MASTER_DATA; never invent roles, tools, dates, degrees, employers, or metrics.
2. Tailor for this job posting using exact job keywords where accurate.
3. Keep resume focused and concise:
   - 4 to 6 sentence summary.
   - 4 to 6 most relevant experience entries only (recent/relevant first).
   - 3 to 5 bullets per experience.
   - 12 to 20 skills, prioritized for this job.
   - Up to 2 most relevant flagship projects.
4. Keep dates, company names, and role titles accurate.
5. Avoid generic filler language.

Required output schema:
{{
  "personal": {{
    "full_name": "...",
    "preferred_title": "...",
    "phone": "...",
    "email": "...",
    "linkedin": "...",
    "github": "...",
    "personal_website": "..."
  }},
  "summary": "...",
  "experience": [
    {{
      "company": "...",
      "title": "...",
      "start_date": "...",
      "end_date": "...",
      "bullets": ["...", "..."]
    }}
  ],
  "education": [
    {{
      "degree": "...",
      "institution": "...",
      "location": "...",
      "dates": "..."
    }}
  ],
  "skills": ["...", "..."],
  "projects": [
    {{
      "name": "...",
      "description": "...",
      "technologies": ["...", "..."]
    }}
  ]
}}

MASTER_DATA:
{json.dumps(master, indent=2)}

JOB_POSTING:
{job_text}
"""


def build_cover_prompt(master: dict[str, Any], job_text: str, today: str) -> str:
    return f"""
You are a strict cover letter writer. Output ONLY valid JSON, no markdown.

Rules:
1. Use only facts from MASTER_DATA and JOB_POSTING.
2. Length target: 220-320 words.
3. Keep tone confident and specific; avoid buzzword-heavy filler.
4. Include concrete fit evidence from recent/relevant work and projects.
5. Do not invent company details that are not in the posting.
6. Use the exact date string: "{today}".

Required output schema:
{{
  "header": {{
    "name": "...",
    "address": "...",
    "phone": "...",
    "email": "...",
    "date": "{today}",
    "employer_address": "..."
  }},
  "salutation": "Dear Hiring Manager,",
  "intro": "...",
  "body": ["...", "..."],
  "conclusion": "...",
  "sign_off": "Sincerely,\\nSean Luka Girgis"
}}

MASTER_DATA:
{json.dumps(master, indent=2)}

JOB_POSTING:
{job_text}
"""


def generate_resume_json(grok: GrokClient, master: dict[str, Any], job_text: str) -> dict[str, Any]:
    response = grok.chat(
        messages=[{"role": "user", "content": build_resume_prompt(master, job_text)}],
        temperature=0.0,
        max_tokens=6000,
    )
    return extract_json(response)


def generate_cover_json(grok: GrokClient, master: dict[str, Any], job_text: str) -> dict[str, Any]:
    today = datetime.now().strftime("%B %d, %Y")
    response = grok.chat(
        messages=[{"role": "user", "content": build_cover_prompt(master, job_text, today)}],
        temperature=0.2,
        max_tokens=2200,
    )
    return extract_json(response)


def run_renderer(script_path: Path, args: list[str]) -> None:
    cmd = [sys.executable, str(script_path), *args]
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run(cmd, check=True, env=env, cwd=str(DATA_ROOT.parent))


def main() -> None:
    global DATA_ROOT, MASTER_ROOT, JOB_ROOT

    parser = argparse.ArgumentParser(description="Direct one-command resume + cover generator")
    parser.add_argument("--job", required=True, help="Job folder name, UUID, or UUID prefix")
    parser.add_argument("--version", default="direct-v1", help="Version tag for generated files")
    parser.add_argument("--model", default="grok-3", help="xAI model")
    parser.add_argument(
        "--data-root",
        default="data",
        help="Root data directory (e.g. data or D:\\StudyBook\\data)",
    )
    parser.add_argument("--skip-cover", action="store_true", help="Generate resume only")
    args = parser.parse_args()

    DATA_ROOT = Path(args.data_root).resolve()
    MASTER_ROOT = DATA_ROOT / "master"
    JOB_ROOT = DATA_ROOT / "jobs"

    if not JOB_ROOT.is_dir():
        raise FileNotFoundError(f"Job root not found: {JOB_ROOT}")

    job_folder = resolve_job_folder(args.job)
    generated_dir = job_folder / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    master = load_master_datastore()
    job_text = load_job_text(job_folder)
    grok = GrokClient(model=args.model)

    resume_json = generate_resume_json(grok, master, job_text)
    resume_path = generated_dir / f"resume_intermediate_{args.version}.json"
    with resume_path.open("w", encoding="utf-8") as f:
        json.dump(resume_json, f, indent=2, ensure_ascii=False)
    print(f"Saved {resume_path}")

    run_renderer(
        PROJECT_ROOT / "scripts" / "05_render_resume.py",
        ["--uuid", job_folder.name, "--version", args.version, "--trim"],
    )

    if not args.skip_cover:
        cover_json = generate_cover_json(grok, master, job_text)
        cover_path = generated_dir / f"cover_intermediate_{args.version}.json"
        with cover_path.open("w", encoding="utf-8") as f:
            json.dump(cover_json, f, indent=2, ensure_ascii=False)
        print(f"Saved {cover_path}")

        run_renderer(
            PROJECT_ROOT / "scripts" / "08_render_cover_letter.py",
            ["--uuid", job_folder.name, "--version", args.version],
        )

    print("Direct generation complete.")


if __name__ == "__main__":
    main()
