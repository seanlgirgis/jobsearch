# scripts/test_ingestion.py
# Run with: python -m scripts.test_ingestion
# Updated for YAML files (2026 version) — supports comments, full history & detailed skills

from pathlib import Path
import re
import yaml
from typing import List, Dict, Any, Optional
#python -m scripts.test_ingestion
# ────────────────────────────────────────────────
# Paths — adjust if your folder structure is different
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent   # repo root if script is in scripts/
DATA_DIR = BASE_DIR / "data" / "master"

MASTER_MD   = DATA_DIR / "master_profile.md"          # optional fallback / raw text source
CAREER_YAML = DATA_DIR / "master_career_data.yaml"
SKILLS_YAML = DATA_DIR / "skills.yaml"


def load_markdown_chunks(path: Path, min_length: int = 50) -> List[str]:
    """Improved markdown splitter: captures sections better (h1–h3)"""
    if not path.is_file():
        print(f"File not found: {path}")
        return []

    text = path.read_text(encoding="utf-8")
    # Split before each header, keep header with content
    chunks = re.split(r'(^#{1,3}\s+.+?$)', text, flags=re.MULTILINE)

    result = []
    current = ""
    for part in chunks:
        stripped = part.strip()
        if stripped.startswith(('#')):
            if current.strip() and len(current.strip()) >= min_length:
                result.append(current.strip())
            current = stripped
        else:
            current += "\n" + part  # preserve original whitespace somewhat

    if current.strip() and len(current.strip()) >= min_length:
        result.append(current.strip())

    return result


def extract_experience_bullets(chunks: List[str]) -> List[str]:
    """Look for experience-like sections and pull bullet lines"""
    bullets = []
    in_experience = False

    for chunk in chunks:
        lower = chunk.lower()
        if any(kw in lower for kw in ["experience", "professional experience", "work history"]):
            in_experience = True

        if in_experience:
            lines = chunk.splitlines()
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(("- ", "* ", "• ", "1. ", "2. ")):  # more bullet styles
                    bullets.append(stripped)

    return bullets


def print_sample_experience(bullets: List[str], max_show: int = 10):
    print(f"\n=== Sample Experience Bullets (showing first {max_show} of {len(bullets)}) ===")
    for i, bullet in enumerate(bullets[:max_show], 1):
        print(f"{i:2d}. {bullet}")
    if len(bullets) > max_show:
        print(f"    ... ({len(bullets) - max_show} more)")


def print_career_summary(career: Dict):
    """Pretty-print key parts of master_career_data.yaml"""
    print("\n=== Career Data Summary ===")
    if not career:
        print("No career data loaded.")
        return

    print(f"Name: {career.get('personal', {}).get('name', 'N/A')}")
    print(f"Current Title: {career.get('personal', {}).get('title', 'N/A')}")
    print(f"Location: {career.get('personal', {}).get('location', 'N/A')}")

    exp = career.get('experience', [])
    print(f"\nExperience Entries: {len(exp)}")
    if exp:
        print("Most recent role:")
        latest = exp[0]
        print(f"  • {latest.get('role', '?')} at {latest.get('company', '?')}")
        print(f"  • {latest.get('start', '?')} – {latest.get('end', '?')}")
        highlights = latest.get('highlights', [])
        if highlights:
            print("    Sample highlights:")
            for h in highlights[:3]:
                print(f"      - {h[:80]}{'...' if len(h) > 80 else ''}")

    projects = career.get('flagship_projects', [])
    print(f"Flagship Projects: {len(projects)}")


def print_top_skills(skills_data: List[Dict], top_n: int = 12):
    """Pretty-print sorted skills with more fields"""
    if not skills_data or not isinstance(skills_data, list):
        print("Skills data not in expected list[dict] format.")
        return

    print(f"\n=== Top {top_n} Skills by Years of Experience ===")
    
    sorted_skills = sorted(
        (s for s in skills_data if isinstance(s.get("years"), (int, float))),
        key=lambda s: s.get("years", 0),
        reverse=True
    )

    for i, skill in enumerate(sorted_skills[:top_n], 1):
        name = skill.get("name", "???")
        years = skill.get("years", "?")
        prof = skill.get("proficiency", "").strip()
        last = skill.get("last_used", "?")
        cats = ", ".join(skill.get("categories", [])) if skill.get("categories") else ""
        extra = f" ({prof})" if prof else ""
        cat_str = f"  [{cats}]" if cats else ""
        print(f"{i:2d}. {name:<28} {years:>2} yrs{extra:<12} last: {last}{cat_str}")


def main():
    print("=== Master Files Ingestion Test (YAML Edition) ===\n")
    
    # 1. Markdown (optional fallback / raw bullets)
    chunks = load_markdown_chunks(MASTER_MD)
    print(f"Loaded master_profile.md → {len(chunks)} chunks")
    
    bullets = extract_experience_bullets(chunks)
    print(f"Extracted {len(bullets)} experience-style bullets")
    print_sample_experience(bullets)
    
    # 2. Career YAML
    career = {}
    try:
        with CAREER_YAML.open(encoding="utf-8") as f:
            career = yaml.safe_load(f) or {}
        print(f"Loaded {CAREER_YAML.name} → type: dict, top-level keys: {list(career.keys())}")
        print_career_summary(career)
    except Exception as e:
        print(f"Error loading career YAML: {e}")
    
    # 3. Skills YAML
    skills = []
    try:
        with SKILLS_YAML.open(encoding="utf-8") as f:
            skills = yaml.safe_load(f) or []
        print(f"Loaded {SKILLS_YAML.name} → {len(skills)} skill entries")
        print_top_skills(skills)
    except Exception as e:
        print(f"Error loading skills YAML: {e}")


if __name__ == "__main__":
    main()