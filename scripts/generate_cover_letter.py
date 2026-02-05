#!/usr/bin/env python3
"""
scripts/generate_cover_letter.py

Generate tailored cover letter text using LLM, then render to MD/DOCX.
Uses strict narrative prompt for coherence.

Usage:
    python scripts/generate_cover_letter.py --uuid <uuid> --version v1 --llm grok
"""

import argparse
import json
import yaml
from pathlib import Path
from datetime import datetime
from docx import Document
from docx.shared import Pt

from src.ai.grok_client import GrokClient  # Your Grok API wrapper

JOB_ROOT = Path("data/jobs")
MASTER_ROOT = Path("data/master")

# Locked Cover Letter Prompt (Variation 1)
COVER_PROMPT = """
You are an expert cover letter writer for staff/senior data engineering roles. Your ONLY task is to generate a personalized, ATS-friendly cover letter.

CRITICAL RULES — VIOLATE ANY AND OUTPUT IS INVALID:
- Structure EXACTLY: Opening paragraph, 2 body paragraphs, closing paragraph + sign-off.
- Length: 350–450 words total; concise, focused, no fluff.
- Tone: First-person, professional, confident, enthusiastic.
- Content: Highlight 4–6 most relevant achievements/projects from master (quantified where possible); weave in job keywords naturally (ELT pipelines, dimensional modeling, data governance, Airflow, orchestration, warehouse technologies).
- Personalization: Reference company ("Collective Health") and role specifics ("Staff Data Engineer", "ingestion and modeling layer", "technical leadership without people management").
- No fabrication: ONLY facts from master career data and job description.
- Do NOT include resume content, JSON, headings, or explanations.

MASTER CAREER DATA: {master_career_data}
JOB DATA: {job_data}

Start with: "Dear Hiring Manager,"

End with: "Best regards,\nSean Luka Girgis\n214-315-2190\nseanlgirgis@gmail.com\nhttps://www.linkedin.com/in/sean-girgis-43bb1b5/"

Output ONLY the plain text cover letter — NOTHING ELSE.
"""

def load_master():
    with open(MASTER_ROOT / "master_career_data.json", "r") as f:
        career_data = json.load(f)
    return career_data

def load_job(uuid_str: str):
    job_dir = JOB_ROOT / uuid_str
    with open(job_dir / "tailored" / "tailored_data_v1.yaml", "r") as f:
        job_data = yaml.safe_load(f)
    return job_data

def generate_tailored_letter(uuid_str: str, llm: str = "grok"):
    master_career = load_master()
    job_data = load_job(uuid_str)

    prompt = COVER_PROMPT.format(
        master_career_data=json.dumps(master_career, indent=2),
        job_data=yaml.safe_dump(job_data, sort_keys=False)
    )

    if llm == "grok":
        client = GrokClient()
        response = client.query(prompt, model="grok-beta", temperature=0.2, max_tokens=1000)  # Slightly higher temp for narrative flow
    else:
        raise NotImplementedError(f"LLM {llm} not implemented.")

    # Response is plain text — no JSON parse needed
    return response.strip()

def render_md(letter_text: str) -> str:
    return f"# Tailored Cover Letter\n\n{letter_text}"

def render_docx(letter_text: str, out_path: Path):
    doc = Document()
    for para in letter_text.split("\n\n"):
        doc.add_paragraph(para)
    # Style tweaks
    for p in doc.paragraphs:
        p.style.font.name = "Arial"
        p.style.font.size = Pt(11)
    doc.save(out_path)

def main():
    parser = argparse.ArgumentParser(description="Generate tailored cover letter")
    parser.add_argument("--uuid", required=True, help="Job UUID")
    parser.add_argument("--version", default="v1", help="Version tag")
    parser.add_argument("--llm", default="grok", help="LLM (grok default)")
    args = parser.parse_args()

    job_dir = JOB_ROOT / args.uuid / "generated"
    job_dir.mkdir(parents=True, exist_ok=True)

    letter_text = generate_tailored_letter(args.uuid, args.llm)

    txt_path = job_dir / f"cover_letter_{args.version}.txt"
    with open(txt_path, "w") as f:
        f.write(letter_text)

    md_path = job_dir / f"cover_letter_{args.version}.md"
    md_content = render_md(letter_text)
    with open(md_path, "w") as f:
        f.write(md_content)

    docx_path = job_dir / f"cover_letter_{args.version}.docx"
    render_docx(letter_text, docx_path)

    print(f"Generated: {txt_path}, {md_path}, {docx_path}")

if __name__ == "__main__":
    main()