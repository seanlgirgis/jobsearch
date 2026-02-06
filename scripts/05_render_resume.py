#!/usr/bin/env python3
"""
scripts/05_render_resume.py

Phase 5 in POC pipeline:
After intermediate JSON is generated → render to Markdown preview and DOCX.
Supports trimming (5 recent jobs) and --all mode.

Fixed:
- Correct hyperlink relationship handling using doc.part
- Pass doc to add_hyperlink
- Minor robustness improvements

Dependencies: pip install python-docx docx2pdf (optional for PDF)
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any, Set

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.shared import OxmlElement, qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

try:
    from docx2pdf import convert
    HAS_PDF = True
except ImportError:
    HAS_PDF = False
    print("Warning: docx2pdf not installed — PDF output disabled. Run: pip install docx2pdf")

JOB_ROOT = Path("data/jobs")
MASTER_ROOT = Path("data/master")


def resolve_job_folder(uuid_str: str) -> Path:
    uuid_str = uuid_str.strip()
    job_dir = JOB_ROOT / uuid_str
    if job_dir.is_dir():
        return job_dir

    candidates = list(JOB_ROOT.glob(f"*_{uuid_str}*"))
    if not candidates:
        short = uuid_str[:8]
        candidates = list(JOB_ROOT.glob(f"*_{short}*"))

    if len(candidates) == 1:
        print(f"Resolved → {candidates[0].name}")
        return candidates[0]
    elif len(candidates) > 1:
        print("Ambiguous UUID:")
        for c in candidates: print(f"  - {c.name}")
        raise ValueError("Ambiguous UUID")
    else:
        raise ValueError(f"Job folder not found for '{uuid_str}'")


def load_latest_intermediate(job_dir: Path, version: str) -> Dict[str, Any]:
    generated_dir = job_dir / "generated"
    if not generated_dir.is_dir():
        raise FileNotFoundError(f"No generated/ folder: {generated_dir}")

    exact = generated_dir / f"resume_intermediate_{version}.json"
    if exact.is_file():
        print(f"Using: {exact.name}")
        with open(exact, encoding="utf-8") as f:
            return json.load(f)

    files = sorted(generated_dir.glob("resume_intermediate_*.json"), reverse=True)
    if not files:
        raise FileNotFoundError("No intermediate JSON found")

    latest = files[0]
    print(f"Fallback to latest: {latest.name}")
    with open(latest, encoding="utf-8") as f:
        return json.load(f)


def load_exclusions() -> Set[str]:
    # Use source_of_truth.json as the master record
    path = Path("data/source_of_truth.json")
    if not path.is_file():
        # Fallback to legacy location just in case
        path = MASTER_ROOT / "master_career_data.json"
        if not path.is_file():
            return set()
            
    with open(path, encoding="utf-8") as f:
        master = json.load(f)
        
    # Check both keys to be safe (source_of_truth has 'experiences', legacy has 'experience')
    exps = master.get("experiences") or master.get("experience", [])
    
    excluded = {
        exp.get("company", "").lower()
        for exp in exps
        if exp.get("exclude_from_resume", False)
    }
    if excluded:
        print(f"Excluding: {', '.join(excluded)}")
    return excluded


def clean_url_for_display(url: str) -> str:
    if not url:
        return ""
    return url.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/") or url


def render_markdown(tailored: Dict, trim: bool = False, exclusions: Set[str] = set()) -> str:
    md = "# Tailored Resume Preview\n\n"

    p = tailored.get("personal", {})
    md += f"**{p.get('full_name', 'Name Missing')}**  \n"
    if p.get("preferred_title"):
        md += f"{p['preferred_title']}  \n"
    md += f"{p.get('phone', '')} | {p.get('email', '')}  \n"

    links = []
    for k, label in [("linkedin", "LinkedIn"), ("github", "GitHub"), ("personal_website", "Portfolio"), ("portfolio", "Portfolio")]:
        if p.get(k):
            links.append(f"[{label}]({p[k]})")
    if links:
        md += " | ".join(links) + "  \n\n"

    md += "## Professional Summary\n" + tailored.get("summary", "N/A") + "\n\n"

    exps = [e for e in tailored.get("experience", []) if e.get("company", "").lower() not in exclusions]
    md += "## Professional Experience\n"
    # Logic:
    # If trim=True: Show top 5 detailed ONLY. (User requested to eliminate "Additional Experience" section)
    # If trim=False (Full): Show ALL detailed.
    shown = exps[:5] if trim else exps
    for e in shown:
        md += f"### {e.get('title', 'Title')} at {e.get('company', 'Company')}\n"
        md += f"{e.get('start_date', '?')} – {e.get('end_date', '?')}\n"
        for b in e.get("bullets", []):
            md += f"- {b}\n"
        md += "\n"

    md += "## Education\n"
    for edu in tailored.get("education", []):
        md += f"**{edu.get('degree', 'Degree')}**  \n{edu.get('institution', '')}"
        if edu.get("location"):
            md += f", {edu['location']}"
        dates = edu.get("dates", "")
        if dates.strip() and dates.lower() not in ["not specified", ""]:
            md += f" ({dates})"
        md += "\n\n"

    md += "## Skills\n" + ", ".join(
        s.get("name", s) if isinstance(s, dict) else s for s in tailored.get("skills", [])
    ) + "\n\n"

    projs = tailored.get("projects", []) or tailored.get("flagship_projects", [])
    if projs:
        md += "## Flagship Projects\n"
        for proj in projs:
            md += f"### {proj.get('name', 'Project')}\n{proj.get('description', '')}\n"
            if proj.get("technologies"):
                md += f"**Technologies:** {', '.join(proj['technologies'])}\n"
            if repo := proj.get("repo"):
                md += f"**Repo:** [{clean_url_for_display(repo)}]({repo})\n"
            md += "\n"

    return md


def add_hyperlink(paragraph, url: str, text: str):
    """Add clickable hyperlink using the document part."""
    if not url or not text:
        return

    part = paragraph.part
    r_id = part.relate_to(url, RT.HYPERLINK, is_external=True)

    hyper = OxmlElement('w:hyperlink')
    hyper.set(qn('r:id'), r_id)

    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0000FF')
    rPr.append(color)

    underline = OxmlElement('w:u')
    underline.set(qn('w:val'), 'single')
    rPr.append(underline)

    r.append(rPr)

    t = OxmlElement('w:t')
    t.text = text
    r.append(t)

    hyper.append(r)
    paragraph._p.append(hyper)


def render_docx(tailored: Dict, out_path: Path, trim: bool = False, exclusions: Set[str] = set()):
    doc = Document()

    p_data = tailored.get("personal", {})
    name_p = doc.add_paragraph()
    name_p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = name_p.add_run(p_data.get("full_name", "Name Missing"))
    run.bold = True
    run.font.size = Pt(16)

    if title := p_data.get("preferred_title"):
        title_p = doc.add_paragraph(title)
        title_p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    contact_p = doc.add_paragraph()
    contact_p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    contact_p.add_run(f"{p_data.get('phone', '')} | {p_data.get('email', '')}")

    # Links - logic to add separator only BETWEEN items
    links_to_add = []
    for key, label in [("linkedin", "LinkedIn"), ("github", "GitHub"), ("personal_website", "Portfolio"), ("portfolio", "Portfolio")]:
        if url := p_data.get(key):
            links_to_add.append((url, label))
    
    if links_to_add:
        # Create a separate paragraph for links
        links_p = doc.add_paragraph()
        links_p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        links_p.paragraph_format.space_before = Pt(0)
        links_p.paragraph_format.space_after = Pt(6)
        
        for i, (url, label) in enumerate(links_to_add):
            if i > 0:
                links_p.add_run(" | ")
            # Use label as text (e.g. "LinkedIn")
            add_hyperlink(links_p, url, label)

    doc.add_heading("Professional Summary", 1)
    doc.add_paragraph(tailored.get("summary", "N/A"))

    exps = [e for e in tailored.get("experience", []) if e.get("company", "").lower() not in exclusions]
    doc.add_heading("Professional Experience", 1)
    
    # Logic:
    # If trim=True: Show top 5 detailed ONLY. (User requested to eliminate "Additional Experience" section)
    # If trim=False (Full): Show ALL detailed.
    
    shown = exps[:5] if trim else exps
    for e in shown:
        p = doc.add_paragraph()
        run = p.add_run(f"{e.get('title', 'Title')} at {e.get('company', 'Company')}")
        run.bold = True
        p.add_run(f" ({e.get('start_date', '?')} – {e.get('end_date', '?')})")
        for b in e.get("bullets", []):
            doc.add_paragraph(b, style="List Bullet")

    doc.add_heading("Education", 1)
    for edu in tailored.get("education", []):
        p = doc.add_paragraph()
        run = p.add_run(edu.get("degree", "Degree"))
        run.bold = True
        line = f"\n{edu.get('institution', '')}"
        if edu.get("location"):
            line += f", {edu['location']}"
        dates = edu.get("dates", "")
        if dates.strip() and dates.lower() not in ["not specified", ""]:
            line += f" ({dates})"
        p.add_run(line)

    doc.add_heading("Skills", 1)
    skills = ", ".join(s.get("name", s) if isinstance(s, dict) else s for s in tailored.get("skills", []))
    doc.add_paragraph(skills)

    projs = tailored.get("projects", []) or tailored.get("flagship_projects", [])
    if projs:
        doc.add_heading("Flagship Projects", 1)
        for proj in projs:
            p = doc.add_paragraph()
            run = p.add_run(proj.get("name", "Project"))
            run.bold = True
            if desc := proj.get("description", ""):
                p.add_run(f"\n{desc.replace('. ', '.\n')}")
            if tech := proj.get("technologies", []):
                p.add_run("\n")
                rt = p.add_run("Technologies: ")
                rt.bold = True
                p.add_run(", ".join(tech))
            if repo := proj.get("repo", ""):
                p.add_run("\n")
                rr = p.add_run("Repo: ")
                rr.bold = True
                add_hyperlink(p, repo, clean_url_for_display(repo))

    for section in doc.sections:
        section.top_margin = section.bottom_margin = Inches(0.5)
        section.left_margin = section.right_margin = Inches(0.6)

    for para in doc.paragraphs:
        for run in para.runs:
            run.font.name = "Arial"
            if "Heading" in para.style.name:
                run.font.size = Pt(13)
            elif run.font.size == Pt(16):
                pass
            else:
                run.font.size = Pt(11)

    doc.save(out_path)


def generate_files(tailored: Dict, job_folder: Path, version: str, trim_mode: bool, exclusions: Set[str], to_pdf: bool = False):
    suffix = "_trimmed" if trim_mode else ""
    md_path = job_folder / "generated" / f"resume_preview_{version}{suffix}.md"
    docx_path = job_folder / "generated" / f"resume_{version}{suffix}.docx"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_markdown(tailored, trim=trim_mode, exclusions=exclusions))
    print(f"Markdown → {md_path}")

    render_docx(tailored, docx_path, trim=trim_mode, exclusions=exclusions)
    print(f"DOCX → {docx_path}")

    if to_pdf and HAS_PDF:
        pdf_path = docx_path.with_suffix(".pdf")
        try:
            convert(str(docx_path), str(pdf_path))
            print(f"PDF → {pdf_path}")
        except Exception as e:
            print(f"PDF conversion failed: {e}")
    elif to_pdf:
        print("PDF skipped (install docx2pdf)")


def main():
    parser = argparse.ArgumentParser(description="Render resume from intermediate JSON")
    parser.add_argument("--uuid", required=True)
    parser.add_argument("--version", default="v1")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--trim", action="store_true")
    group.add_argument("--all", action="store_true")
    parser.add_argument("--format", default="docx", choices=["docx", "pdf"])
    args = parser.parse_args()

    job_folder = resolve_job_folder(args.uuid)
    tailored = load_latest_intermediate(job_folder, args.version)
    exclusions = load_exclusions()

    to_pdf = args.format == "pdf"

    if args.all:
        generate_files(tailored, job_folder, args.version, True, exclusions, to_pdf)
        generate_files(tailored, job_folder, args.version, False, exclusions, to_pdf)
    else:
        generate_files(tailored, job_folder, args.version, args.trim, exclusions, to_pdf)

    print("\nDone.")


if __name__ == "__main__":
    main()