#!/usr/bin/env python3
"""
scripts/profile_export.py

Export legacy master files (e.g., master_career_data.json, skills.yaml) from source_of_truth.json.
Run after any source_of_truth updates to keep v0 scripts compatible.

Usage:
    python scripts/profile_export.py
"""
from pathlib import Path
import json
import yaml

DATA_ROOT = Path("data")
SOT_PATH = DATA_ROOT / "source_of_truth.json"
MASTER_DIR = DATA_ROOT / "master"
MASTER_DIR.mkdir(exist_ok=True)

def export_master_career_data(sot: dict) -> None:
    """Extract to master_career_data.json (matches old structure)."""
    career_data = {
        "personal": sot["personal_info"],
        "summary": sot["professional_summary"]["short"],
        "flagship_projects": sot["projects"],
        "experience": [
            {
                "company": exp["company"],
                "title": exp["role"],
                "start_date": exp["start_date"],
                "end_date": exp["end_date"],
                "bullets": exp["highlights"]
            }
            for exp in sot["experiences"]
        ],
        "education": sot["education"]
    }
    out_path = MASTER_DIR / "master_career_data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(career_data, f, indent=2)
    print(f"Exported: {out_path}")

def export_master_career_yaml(sot: dict) -> None:
    """Extract to master_career_data.yaml (matches old YAML structure)."""
    career_yaml = {
        "personal": {
            "name": sot["personal_info"]["full_name"],
            "title": sot["personal_info"]["preferred_title"],
            "location": sot["personal_info"]["location_preference"],
            "email": sot["personal_info"]["email"],
            "phone": sot["personal_info"]["phone"],
            "linkedin": sot["personal_info"]["linkedin"],
            "github": sot["personal_info"]["github"],
            "twitter": sot["personal_info"]["x_twitter"],  # or X
            "website": sot["personal_info"]["personal_website"]
        },
        "summary": {
            "short": sot["professional_summary"]["short"],
            "long": sot["professional_summary"]["long"]
        },
        "experience": [
            {
                "company": exp["company"],
                "role": exp["role"],
                "location": "",  # not in sot; blank for compat
                "start": exp["start_date"],
                "end": exp["end_date"],
                "highlights": exp["highlights"]
            }
            for exp in sot["experiences"]
        ],
        "education": [
            {
                "degree": edu["degree"],
                "school": edu["institution"],
                "location": edu["location"],
                "year": edu["dates"] if edu["dates"] != "Not specified" else "",
                "gpa": None
            }
            for edu in sot["education"]
        ],
        "certifications": sot["certifications"],
        "flagship_projects": sot["projects"]
    }
    out_path = MASTER_DIR / "master_career_data.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(career_yaml, f, sort_keys=False, allow_unicode=True)
    print(f"Exported: {out_path}")

def export_skills_yaml(sot: dict) -> None:
    """Extract to skills.yaml (matches old list format)."""
    skills_list = [
        {
            "name": skill["name"],
            "years": skill["years"],
            "proficiency": skill["proficiency"],
            "last_used": skill["last_used"],
            "categories": [skill["category"]],
            "notes": skill["context"]
        }
        for skill in sot["skills"] if skill["years"] is not None  # Prioritize detailed ones
    ]
    out_path = MASTER_DIR / "skills.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(skills_list, f, sort_keys=False)
    print(f"Exported: {out_path}")

# Add more if loader needs (e.g., skills.json as array, master_profile.md as markdown)

def main():
    if not SOT_PATH.is_file():
        raise FileNotFoundError(f"Missing {SOT_PATH} — run unification first.")
    
    with open(SOT_PATH, "r", encoding="utf-8") as f:
        sot = json.load(f)
    
    export_master_career_data(sot)
    export_master_career_yaml(sot)
    export_skills_yaml(sot)

if __name__ == "__main__":
    main()