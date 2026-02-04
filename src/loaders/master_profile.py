# src/loaders/master_profile.py
"""
Central loader for master personal data.
Loads YAML files as primary source + markdown as fallback/raw text.
Provides query methods for resume tailoring, keyword matching, etc.

Usage:
    from src.loaders.master_profile import MasterProfileLoader

    loader = MasterProfileLoader()
    recent = loader.get_recent_experience(3)
    top_skills = loader.get_top_skills(15)
"""

from pathlib import Path
import yaml
from typing import List, Dict, Any, Optional

# ────────────────────────────────────────────────
# Config / Paths (relative to repo root)
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # repo root
DATA_DIR = BASE_DIR / "data" / "master"

CAREER_PATH = DATA_DIR / "master_career_data.yaml"
SKILLS_PATH = DATA_DIR / "skills.yaml"
PROFILE_MD  = DATA_DIR / "master_profile.md"   # optional fallback


class MasterProfileLoader:
    """Loads and caches master profile data from YAML + markdown."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DATA_DIR
        self.career: Dict[str, Any] = self._load_yaml(CAREER_PATH)
        self.skills: List[Dict[str, Any]] = self._load_yaml(SKILLS_PATH)
        self.md_chunks: List[str] = []  # lazy load if needed

    def _load_yaml(self, path: Path) -> Any:
        if not path.is_file():
            raise FileNotFoundError(f"Missing required file: {path}")
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data or {} if isinstance(data, dict) else data or []

    def get_personal_info(self) -> Dict[str, Any]:
        return self.career.get("personal", {})

    def get_summary(self, variant: str = "short") -> str:
        summaries = self.career.get("summary", {})
        return summaries.get(variant, summaries.get("short", ""))

    def get_experience(self, n: Optional[int] = None) -> List[Dict]:
        exp = self.career.get("experience", [])
        return exp[:n] if n else exp

    def get_recent_experience(self, n: int = 3) -> List[Dict]:
        return self.get_experience(n)

    def get_flagship_projects(self) -> List[Dict]:
        return self.career.get("flagship_projects", [])

    def get_skills(self, min_years: float = 0.0) -> List[Dict]:
        return [s for s in self.skills if s.get("years", 0) >= min_years]

    def get_top_skills(self, n: int = 15, min_years: float = 2.0) -> List[Dict]:
        filtered = self.get_skills(min_years)
        return sorted(
            filtered,
            key=lambda s: (s.get("years", 0), s.get("proficiency", "") == "Expert"),
            reverse=True
        )[:n]

    def get_skill_names(self, n: int = 20) -> List[str]:
        return [s["name"] for s in self.get_top_skills(n)]

    # Optional: lazy markdown chunk loader for raw bullets
    def load_md_chunks(self, min_length: int = 50) -> List[str]:
        if self.md_chunks:
            return self.md_chunks
        if not PROFILE_MD.is_file():
            return []
        text = PROFILE_MD.read_text(encoding="utf-8")
        # simple header-based split (can improve later)
        chunks = []
        current = ""
        for line in text.splitlines():
            if line.strip().startswith("#"):
                if current.strip() and len(current) >= min_length:
                    chunks.append(current.strip())
                current = line
            else:
                current += "\n" + line
        if current.strip() and len(current) >= min_length:
            chunks.append(current.strip())
        self.md_chunks = chunks
        return chunks


# ────────────────────────────────────────────────
# Smoke test / usage demo (run with python -m src.loaders.master_profile)
# ────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== MasterProfileLoader Smoke Test ===\n")

    try:
        loader = MasterProfileLoader()

        print("Personal info:")
        print(loader.get_personal_info())

        print(f"\nShort summary (first 120 chars):")
        print(loader.get_summary()[:120] + "..." if loader.get_summary() else "[none]")

        recent = loader.get_recent_experience(2)
        print(f"\nMost recent {len(recent)} roles:")
        for role in recent:
            print(f"  • {role.get('role')} at {role.get('company')} ({role.get('start')} – {role.get('end')})")

        top_skills = loader.get_top_skills(10)
        print(f"\nTop 10 skills:")
        for s in top_skills:
            print(f"  • {s['name']} ({s.get('years')} yrs, {s.get('proficiency', 'N/A')})")

        print("\nTest successful! Data loaded cleanly.")

    except Exception as e:
        print("Test failed:")
        print(str(e))
        print("\nCommon fixes:")
        print("  • Check data/master/*.yaml files exist")
        print("  • pyyaml installed? (pip install pyyaml)")
        print("  • Paths correct? (data/master/ relative to repo root)")