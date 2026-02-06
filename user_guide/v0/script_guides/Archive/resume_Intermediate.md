Understood — no problem at all. If you feel the separate `tailor_job_data.py` step is dead weight (and hasn't been resurrected in 3 days), we can kill it off entirely and consolidate the tailoring logic **directly into `resume_intermediate.py`**. This simplifies the pipeline: feed a raw job description (or URL) right into intermediate, let the LLM handle full tailoring in one go, then render as usual.

### Quick pipeline update
New flow:
1. Run `resume_intermediate.py --uuid <uuid> --job-description "paste job text here" [--job-url <url>]`  
   → LLM gets master data + raw job input → tailors + outputs JSON
2. Run `resume_generation.py --uuid <uuid> [--all]`

If `--job-description` is missing, it falls back to no tailoring (just master data).

### Updated full `resume_intermediate.py`
I added:
- `--job-description`: Optional string for raw job text (paste the posting).
- `--job-url`: Optional URL (if provided, we can add a browse_page tool call later for fetching, but for now it's placeholder).
- If job_data is empty, prompt warns but proceeds with generic output.
- Prompt updated to handle raw job text directly (LLM extracts keywords/responsibilities itself).

```python
#!/usr/bin/env python3
"""
scripts/resume_intermediate.py
Generates a tailored resume in structured JSON format via LLM (bound to source_of_truth).
Filters out experiences marked with "exclude_from_resume": true.
Now handles raw job description directly for tailoring (no separate tailor step needed).

Usage:
    python scripts/resume_intermediate.py --uuid <uuid> --version v1 [--job-description "job text"] [--job-url <url>] [--model grok-3]
"""
import argparse
import json
import yaml
from pathlib import Path
import re  # For cleaning LLM response if needed

try:
    from src.ai.grok_client import GrokClient
except ImportError:
    print("Warning: src.ai.grok_client not found — entering mock mode.")
    GrokClient = None

JOB_ROOT = Path("data/jobs")
MASTER_ROOT = Path("data/master")

# Updated prompt to handle raw job description (if no YAML)
RESUME_PROMPT_TEMPLATE = """
You are a rule-bound resume optimizer. Temperature=0 for determinism. Violate rules = invalid response.
CHECKLIST (MUST ADHERE 100%):
1. No truncation: Keep all core profile sections (personal, summary, experience, education, skills, projects). Include ALL items from master — do not omit or shorten lists. Keep output concise to fit.
2. Tailor only: Adjust bullets/descriptions to match job keywords — no invention, no date changes, no new facts. Keep bullets short (1-2 lines each).
3. Bind to source_of_truth: Use EXACT dates, roles, companies, degrees from master_career_data. Standardize fields (e.g., 'personal_website').
4. Output JSON only: No other text. Start with {{ and end with }}. Valid JSON object. Ensure the entire JSON is complete — no partial output. If too long, shorten descriptions but include all entries.
5. No creativity in dates/education: Copy verbatim from master.
6. Quantify achievements where possible from master bullets.
7. Tailor summary/experience bullets to job_data (extract responsibilities/requirements from raw text if no structured YAML). Weave in keywords naturally (e.g., 'ELT pipelines', 'dimensional modeling'). Keep summary under 150 words.
8. Keep experience chronological, full history — tailor relevance, not remove. Include ALL experiences from master, with 3-5 bullets each max.
9. Skills: Dedupe, prioritize top matches to job skills. Include ALL skills from master, sorted by relevance, but group if needed to fit.
10. Projects: Include all, tailor descriptions to job. Keep descriptions short (2-3 sentences).

Master career data (JSON) — already filtered to exclude short/irrelevant stints:
{career_json}

Master skills (JSON):
{skills_json}

Job data (raw text or YAML — extract key sections like responsibilities, requirements if raw):
{job_data}

Generate the tailored resume JSON now. Output ONLY the complete JSON object — nothing before or after. Make sure it's fully formed and not truncated. Shorten individual bullets/descriptions if necessary to complete the output.
"""


def load_master() -> tuple[dict, dict]:
    career_path = MASTER_ROOT / "master_career_data.json"
    skills_path = MASTER_ROOT / "skills.yaml"
    if not career_path.is_file() or not skills_path.is_file():
        raise FileNotFoundError(f"Missing master files at {MASTER_ROOT}. Run profile_export.py first.")

    with open(career_path, "r", encoding="utf-8") as f:
        master = json.load(f)

    # Filter out experiences marked for exclusion
    if "experiences" in master:
        original_count = len(master["experiences"])
        master["experiences"] = [
            exp for exp in master["experiences"]
            if not exp.get("exclude_from_resume", False)
        ]
        filtered_count = len(master["experiences"])
        if filtered_count < original_count:
            print(f"Excluded {original_count - filtered_count} experience entries marked 'exclude_from_resume'")

    with open(skills_path, "r", encoding="utf-8") as f:
        skills = yaml.safe_load(f)

    return master, skills


def load_tailored_job(uuid: str, job_description: str, job_url: str) -> str:
    # If job_description provided, use it directly as raw text
    if job_description:
        return job_description  # Raw string for prompt

    # Placeholder for job_url fetch (add browse_page tool if needed later)
    if job_url:
        # For now, warn and return empty
        print(f"Warning: --job-url provided but fetching not implemented yet. Using empty job data.")
        return ""

    # Fallback: try loading existing YAML (for backward compat)
    tailored_dir = JOB_ROOT / uuid / "tailored"
    tailored_path = tailored_dir / "tailored_data_v1.yaml"
    if tailored_path.is_file():
        with open(tailored_path, "r", encoding="utf-8") as f:
            return yaml.dump(yaml.safe_load(f), sort_keys=False, allow_unicode=True)
    else:
        print("Warning: No --job-description, --job-url, or existing tailored YAML. Tailoring will be minimal.")
        return ""  # Empty job data → generic output


def call_llm(prompt: str, model: str = "grok-3") -> dict:
    if GrokClient is None:
        print("Using mock response (GrokClient not available).")
        return {
            "personal": {"full_name": "Sean Luka Girgis", "email": "seanlgirgis@gmail.com"},
            "summary": "Mock tailored summary",
            "experience": [{"company": "Mock Co", "title": "Mock Role", "bullets": ["Mock bullet"]}],
            "education": [{"degree": "Mock Degree", "institution": "Mock Univ"}],
            "skills": ["python", "sql"],
            "projects": [{"name": "Mock Project", "description": "Mock desc"}]
        }

    grok = GrokClient(model=model)
    print("Calling Grok...")
    response = grok.chat([{"role": "user", "content": prompt}], max_tokens=8192)

    print("Raw LLM response (first 800 chars):")
    print(response[:800])
    print("... (end of preview)")

    # Clean response: extract JSON block if wrapped
    json_str = response.strip()
    json_match = re.search(r'\{.*\}', json_str, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print("Failed to parse response as JSON. Raw content:")
        print(response)
        raise ValueError("LLM did not return valid JSON. Check raw response above and prompt.")


def main():
    parser = argparse.ArgumentParser(description="Generate resume intermediate JSON via LLM")
    parser.add_argument("--uuid", required=True, help="Job UUID")
    parser.add_argument("--version", default="v1", help="Version tag")
    parser.add_argument("--job-description", default="", help="Raw job description text for tailoring (paste here)")
    parser.add_argument("--job-url", default="", help="Job posting URL (fetching not yet implemented)")
    parser.add_argument("--model", default="grok-3", help="Grok model")
    args = parser.parse_args()

    job_dir = JOB_ROOT / args.uuid / "generated"
    job_dir.mkdir(parents=True, exist_ok=True)

    # Load data (with exclusion filter applied)
    master_career, master_skills = load_master()
    job_data = load_tailored_job(args.uuid, args.job_description, args.job_url)

    # Build prompt
    prompt_text = RESUME_PROMPT_TEMPLATE.format(
        career_json=json.dumps(master_career, indent=2),
        skills_json=json.dumps(master_skills, indent=2),
        job_data=job_data  # Raw text or YAML dump
    )

    print("Generating resume intermediate...")
    tailored = call_llm(prompt_text, args.model)

    json_path = job_dir / f"resume_intermediate_{args.version}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tailored, f, indent=2, ensure_ascii=False)
    print(f"Saved intermediate JSON → {json_path}")

    print("\nNext: Review/edit the JSON file manually if needed.")
    print(f"Then run: python scripts/resume_generation.py --uuid {args.uuid} --version {args.version} [--all]")


if __name__ == "__main__":
    main()
```

### How to test it
1. Run with a job description:  
   ```bash
   python scripts/resume_intermediate.py --uuid test-uuid --job-description "Senior Data Engineer role: Build ELT pipelines in AWS, use PySpark for big data, Airflow orchestration, 5+ years exp..." --version v1
   ```
   → LLM tailors based on that text.

2. Without description (generic):  
   ```bash
   python scripts/resume_intermediate.py --uuid test-uuid --version v1
   ```

3. Then generate:  
   ```bash
   python scripts/resume_generation.py --uuid test-uuid --version v1 --all
   ```

This keeps the pipeline simple (2 steps max). If you want to add URL fetching (using browse_page tool), we can — just say the word. Let me know how this runs or what to tweak next.