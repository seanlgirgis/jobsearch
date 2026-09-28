"""Build/check the compact public candidate context, without LLM calls or source edits."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIRECTOR = ROOT.parent / "Grok_DIRECTOR"
PROFILE_PATH = Path("data/master/candidate_profile_runtime.json")
REPORT_PATH = Path("data/master/candidate_profile_runtime_validation.md")
MAX_PROFILE_BYTES = 12000
REQUIRED = {
    "career": "data/master/master_career_data.yaml",
    "skills": "data/master/skills.yaml",
    "current_work": "data/master/bofa_stated_ai_work.md",
    "positioning": "outbox/sean_girgis_searchable_profile.md",
    "guardrails": "PROJECT_MEMORY.md",
    "rules": "config/runtime_profile_rules.json",
}
FOUNDATIONS = [
    "Databricks",
    "Delta Lake",
    "dbt",
    "Snowflake",
    "Unity Catalog",
    "Delta Live Tables",
    "Azure (Data Platform Foundations)",
    "Databricks Workflows",
    "Medallion Architecture",
    "Data Vault",
]
PUBLIC_SAFETY = {
    "current_employer": "LTIMindtree",
    "client": "Never name the current client or include its data, prompts, URLs or unlisted tools.",
    "research": "CAPTAIN is research/investigation, not production. Omit its codename in public documents.",
    "foundation_limit": "Foundational-only skills, including DLT and Azure data-platform foundations, are not professional production expertise.",
    "accuracy": "Never invent titles, dates, metrics, certifications or production status; null means unconfirmed.",
    "current_role_metrics": "Omit unconfirmed report-time savings, annual volumes, derived annual savings and Power BI report counts.",
    "positioning": "Do not position the candidate as a generic data-science or ML specialist.",
    "privacy": "Exclude private biography, credentials, internal implementation details, file paths and URLs.",
    "evidence": "Master and user-stated claims are source-backed, not independently verified. Skill tiers are source labels, not credentials or proof of current production use.",
}
URL_OR_PATH = re.compile(
    r"(?i)(?:\b(?:https?|ftp|file)://|www\.|[a-z]:[\\/]|\\\\|"
    r"\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|ai|internal|local)\b)"
)
CREDENTIAL = re.compile(
    r"(?i)\b(?:sk-[\w-]{8,}|xai-[\w-]{8,}|AKIA[A-Z0-9]{16}|bearer\s+\S+)|BEGIN.*PRIVATE KEY"
)
FOUNDATION_WORDING = re.compile(
    r"(?i)\b(?:databricks|delta\s+lake|dbt|snowflake|unity\s+catalog|"
    r"delta\s+live\s+tables|dlt|azure|medallion\s+architecture|data\s+vault)\b"
)


class RuntimeProfileError(ValueError):
    """A concise error without echoing private source content."""


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def read_sources(root: Path, director_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sources: dict[str, Any] = {}
    provenance = []
    paths = {key: root / path for key, path in REQUIRED.items()}
    paths.update(
        {
            "director_identity": director_dir / "SEAN.md",
            "director_now": director_dir / "SEAN_NOW.md",
        }
    )
    for key, path in paths.items():
        try:
            raw = path.read_bytes()
        except FileNotFoundError:
            if key.startswith("director_"):
                provenance.append(
                    {"id": key, "path": path.name, "status": "optional source absent"}
                )
                continue
            raise RuntimeProfileError(f"Required source missing: {REQUIRED[key]}") from None
        except OSError:
            raise RuntimeProfileError(f"Cannot read source: {key}") from None
        try:
            text = raw.decode("utf-8-sig")
            value = (
                yaml.safe_load(text)
                if path.suffix == ".yaml"
                else json.loads(text) if key == "rules" else text
            )
        except (ValueError, UnicodeError, yaml.YAMLError):
            raise RuntimeProfileError(f"Invalid source encoding or syntax: {key}") from None
        sources[key] = value
        provenance.append(
            {
                "id": key,
                "path": REQUIRED.get(key, path.name),
                "bytes": len(raw),
                "sha256": digest(raw),
            }
        )
    if not isinstance(sources["career"], dict) or not isinstance(sources["skills"], list):
        raise RuntimeProfileError("Career must be a YAML object and skills must be a YAML list.")
    if not isinstance(sources["rules"], dict) or sources["rules"].get("version") != 1:
        raise RuntimeProfileError("Unsupported runtime projection rules.")
    return sources, provenance


def table_field(text: str, name: str) -> str | None:
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0].casefold() == name.casefold():
            return cells[1]
    return None


def public_identity(sources: dict[str, Any]) -> dict[str, str]:
    personal = sources["career"].get("personal", {})
    director = sources.get("director_identity", "")
    identity = {
        "name": table_field(director, "Name") or personal.get("name"),
        "location": table_field(director, "Lives") or personal.get("location"),
        "email": personal.get("email"),
        "phone": personal.get("phone"),
    }
    if any(
        not isinstance(value, str) or not value.strip() or len(value) > 150
        for value in identity.values()
    ):
        raise RuntimeProfileError(
            "Public name, location, email and phone are required and must be concise."
        )
    employer = table_field(director, "Employer")
    if employer is not None and employer.split("(", 1)[0].strip() != "LTIMindtree":
        raise RuntimeProfileError(
            "Current employer evidence changed; review public-employer rules."
        )
    if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", identity["email"]):
        raise RuntimeProfileError("Public contact email is invalid.")
    return identity


def collect_evidence(
    sources: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    rules = sources["rules"]
    actual = digest(sources["current_work"].replace("\r\n", "\n").encode("utf-8"))
    if actual != rules["current_work_sha256"]:
        raise RuntimeProfileError(
            "Current-work evidence changed; review the sanitized bullets before rebuilding."
        )
    evidence = []
    bank = []
    for rule in rules["evidence"]:
        kind = rule["kind"]
        item: dict[str, Any] = {"id": rule["id"], "kind": kind}
        if kind == "current":
            item.update(
                employer="LTIMindtree",
                function=rule["function"],
                official_title=None,
                start_date=None,
                end_date=None,
                current=True,
                status=rule["status"],
            )
        else:
            collection, field = (
                ("experience", "company") if kind == "experience" else ("flagship_projects", "name")
            )
            matches = [
                entry
                for entry in sources["career"].get(collection, [])
                if entry.get(field) == rule["match"]
            ]
            if len(matches) != 1 or digest(canonical(matches[0])) != rule["sha256"]:
                raise RuntimeProfileError(
                    f"Selected source evidence changed or is missing: {rule['id']}; review the projection rules."
                )
            entry = matches[0]
            if kind == "experience":
                item.update(
                    employer=rule.get("public_employer", entry["company"]),
                    title=entry["role"],
                    start=entry["start"],
                    end=entry["end"],
                    status="master_record",
                )
            else:
                timeframe = entry.get("timeframe")
                item.update(
                    name=rule.get("public_name", entry["name"]),
                    timeframe=(
                        timeframe
                        if isinstance(timeframe, str) and re.fullmatch(r"\d{4}", timeframe)
                        else None
                    ),
                    status=rule["status"],
                )
        item["bullet_ids"] = [bullet["id"] for bullet in rule["bullets"]]
        evidence.append(item)
        bank.extend(
            {"id": bullet["id"], "evidence": rule["id"], "text": bullet["text"]}
            for bullet in rule["bullets"]
        )
    return evidence, bank


def collect_skills(sources: dict[str, Any], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    rows = sources["skills"]
    if any(not isinstance(row, dict) or not isinstance(row.get("name"), str) for row in rows):
        raise RuntimeProfileError("Invalid skill inventory structure.")
    inventory = {row["name"]: row for row in rows}
    if len(inventory) != len(rows):
        raise RuntimeProfileError("Duplicate skill names require source review.")
    tiers: dict[str, Any] = {}
    evidence_ids = {item["id"] for item in evidence}
    for group, spec in sources["rules"]["skill_groups"].items():
        if not set(spec["evidence"]) <= evidence_ids:
            raise RuntimeProfileError("Skill tier references missing evidence.")
        by_level: dict[str, list[str]] = defaultdict(list)
        for name in spec["names"]:
            row = inventory.get(name)
            if row is None or name in FOUNDATIONS:
                raise RuntimeProfileError(
                    "Required skill missing or foundational skill improperly promoted."
                )
            level = row.get("proficiency")
            if (
                level not in {"Expert", "Advanced", "Intermediate-Advanced", "Intermediate"}
                or row.get("years", 0) <= 0
            ):
                raise RuntimeProfileError(
                    "Selected skill tier changed; review its evidence and projection."
                )
            by_level[level].append(name)
        tiers[group] = dict(by_level)
    if not set(FOUNDATIONS) <= inventory.keys():
        raise RuntimeProfileError("Required foundational skill inventory is incomplete.")
    tiers["foundational_only"] = FOUNDATIONS
    tiers["source_supported_unrated"] = sources["rules"]["unrated_skills"]
    return tiers


def _strings(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [text for key, child in value.items() for text in [str(key), *_strings(child)]]
    if isinstance(value, list):
        return [text for child in value for text in _strings(child)]
    return [value] if isinstance(value, str) else []


def validate_runtime_profile(profile: dict[str, Any]) -> None:
    """Fail closed on private content, missing safeguards, or evidence inconsistencies."""
    rendered = "\n".join(_strings(profile))
    normalized = unicodedata.normalize("NFKC", rendered).casefold()
    compact = re.sub(r"[^a-z0-9]", "", normalized)
    if any(word in compact for word in ("bankofamerica", "bofa", "bofamerica")) or re.search(
        r"\bboa\b", normalized
    ):
        raise RuntimeProfileError(
            "Prohibited client wording in runtime profile; nothing was written."
        )
    identity = profile.get("identity", {})
    # Email is the only allowed public domain-bearing string.
    no_email = rendered.replace(identity.get("email", ""), "")
    if URL_OR_PATH.search(no_email) or CREDENTIAL.search(rendered):
        raise RuntimeProfileError(
            "Prohibited URL, file path or credential pattern in runtime profile."
        )
    if profile.get("public_safety") != PUBLIC_SAFETY:
        raise RuntimeProfileError("Runtime public-safety constraints are incomplete or altered.")
    if set(profile) != {
        "schema_version",
        "identity",
        "positioning",
        "skill_tiers",
        "evidence",
        "bullet_bank",
        "education",
        "public_safety",
        "job_family_keywords",
    }:
        raise RuntimeProfileError("Unexpected or missing runtime sections.")
    if set(identity) != {"name", "location", "email", "phone"}:
        raise RuntimeProfileError(
            "Only public name, location, email and phone belong in runtime identity."
        )
    current = [item for item in profile["evidence"] if item["kind"] == "current"]
    if (
        len(current) != 1
        or current[0]["employer"] != "LTIMindtree"
        or any(
            current[0][field] is not None for field in ("official_title", "start_date", "end_date")
        )
    ):
        raise RuntimeProfileError("Current-employment constraints failed.")
    if profile["skill_tiers"].get("foundational_only") != FOUNDATIONS:
        raise RuntimeProfileError("Foundational skill restrictions are missing.")
    for group, tier in profile["skill_tiers"].items():
        if group != "foundational_only" and FOUNDATION_WORDING.search("\n".join(_strings(tier))):
            raise RuntimeProfileError(
                "Foundational skills must not be promoted into production tiers."
            )
    bank = profile["bullet_bank"]
    ids = [bullet["id"] for bullet in bank]
    if len(set(ids)) != len(ids):
        raise RuntimeProfileError("Duplicate selected-bullet IDs.")
    for item in profile["evidence"]:
        if set(item["bullet_ids"]) != {
            bullet["id"] for bullet in bank if bullet["evidence"] == item["id"]
        }:
            raise RuntimeProfileError("Evidence and selected-bullet references do not match.")
    if any(
        skill["evidence"] not in ids for skill in profile["skill_tiers"]["source_supported_unrated"]
    ):
        raise RuntimeProfileError("Unrated skill references missing evidence.")
    for bullet in bank:
        if FOUNDATION_WORDING.search(bullet["text"]):
            raise RuntimeProfileError(
                "Foundational technology must not be introduced as an accomplishment."
            )
        if bullet["evidence"] == "current" and re.search(r"\d", bullet["text"]):
            raise RuntimeProfileError("Unconfirmed current-role metrics must be omitted.")
    research = [bullet["text"].casefold() for bullet in bank if bullet["id"] == "current_research"]
    if (
        len(research) != 1
        or "research/investigation" not in research[0]
        or "not production" not in research[0]
    ):
        raise RuntimeProfileError(
            "The knowledge-base research must be explicitly qualified as non-production."
        )
    if len(canonical(profile)) > MAX_PROFILE_BYTES:
        raise RuntimeProfileError("Runtime profile exceeds the compact 12,000-byte budget.")


def build_profile(root: Path = ROOT, director_dir: Path = DIRECTOR) -> tuple[dict[str, Any], str]:
    sources, provenance = read_sources(root, director_dir)
    evidence, bank = collect_evidence(sources)
    # Positioning never supplies career facts, dates, proficiency or accomplishment metrics.
    if not all(
        term in sources["positioning"].casefold() for term in ("capacity", "part-time", "evenings")
    ):
        raise RuntimeProfileError(
            "Positioning source changed; review the selected engagement targets."
        )
    education = [
        {"degree": entry["degree"], "school": entry["school"]}
        for entry in sources["career"].get("education", [])
    ]
    profile = {
        "schema_version": 1,
        "identity": public_identity(sources),
        "positioning": sources["rules"]["positioning"],
        "skill_tiers": collect_skills(sources, evidence),
        "evidence": evidence,
        "bullet_bank": bank,
        "education": education,
        "public_safety": PUBLIC_SAFETY,
        "job_family_keywords": sources["rules"]["job_family_keywords"],
    }
    validate_runtime_profile(profile)
    profile_bytes = canonical(profile) + b"\n"
    input_bytes = sum(
        item.get("bytes", 0) for item in provenance if item["id"] not in {"rules", "guardrails"}
    )
    lines = [
        "# Runtime candidate profile validation",
        "",
        f"- Profile: `{PROFILE_PATH.as_posix()}` (derived context; do not hand-edit).",
        f"- Size: {len(profile_bytes):,} UTF-8 bytes; {len(profile_bytes.decode('utf-8')):,} characters.",
        f"- Candidate source inputs: {input_bytes:,} bytes; reduction: {100 * (1 - len(profile_bytes) / input_bytes):.1f}% by bytes (not a token measurement).",
        f"- Profile SHA-256: `{digest(profile_bytes)}`.",
        f"- Evidence groups: {len(evidence)}; selected bullets: {len(bank)}.",
        "- Validation: PASS; prohibited client references 0; URLs, file paths and credential patterns 0.",
        "- Source safety: raw master evidence and Director files are read only; no LLM calls.",
        "",
        "## Source provenance",
        "",
    ]
    for item in provenance:
        lines.append(
            f"- `{item['path']}` ({item['id']}): "
            + (
                f"{item['bytes']:,} bytes; SHA-256 `{item['sha256']}`."
                if "sha256" in item
                else item["status"]
            )
        )
    lines.extend(
        [
            "",
            "## Selection and exclusions",
            "",
            "- Identity: Director name/location when present, otherwise master fields; email and phone from master. Searchable profile is positioning-only. Director current-focus notes add no employment dates or metrics.",
            "- Skills: original source proficiency within professional, project/practical, or historical evidence groups. Years/last-used estimates and unselected inventory notes are omitted. Unrated tools carry bullet references; foundational tools are capped regardless of a future inventory label.",
            "- Current employer: LTIMindtree only. Official title and dates remain null; function is a descriptive label. Current work is user-stated, with research explicitly separated from production.",
            "- Excluded: current client name/abbreviations, private biography, internal prompts/data/tool details, URLs/local paths, unlisted tools, current-role savings/report-volume estimates and their derived annual totals, report counts, and production claims for research.",
            "- Excluded for compactness: most early-career history, obsolete software versions, legacy certification inventory, duplicate bullets, generic ML/DS positioning, uncorroborated skill-only extras and promotional scale comparisons.",
            "- Selected bullet summaries are reviewed projections of fingerprinted evidence. Source evidence changes stop the builder until the summaries and fingerprints are reviewed together; never merely refresh a hash to suppress that check.",
            "- No independent credential verification is claimed. Existing source labels and project metrics remain attributed to their evidence scope.",
            "",
            "## Rebuild and validate",
            "",
            "```powershell",
            ". .\\env_setter.ps1",
            "python scripts\\build_runtime_profile.py",
            "python scripts\\build_runtime_profile.py --check",
            "```",
            "",
        ]
    )
    return profile, "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=ROOT, help="Workspace root (also useful for offline fixtures)"
    )
    parser.add_argument("--director-dir", type=Path, default=DIRECTOR)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate existing derived files and detect stale/tampered content; no writes",
    )
    args = parser.parse_args(argv)
    try:
        profile, report = build_profile(args.root, args.director_dir)
        content = canonical(profile) + b"\n"
        output, report_file = args.root / PROFILE_PATH, args.root / REPORT_PATH
        if args.check:
            if not output.is_file() or not report_file.is_file():
                raise RuntimeProfileError(
                    "Derived profile or report is missing; run the builder first."
                )
            existing = json.loads(output.read_text(encoding="utf-8"))
            validate_runtime_profile(existing)
            if output.read_bytes() != content or report_file.read_text(encoding="utf-8") != report:
                raise RuntimeProfileError(
                    "Derived profile/report is stale or altered; review sources and rebuild."
                )
        else:
            # All source/evidence/safety validation completes before either derived file is written.
            output.write_bytes(content)
            report_file.write_text(report, encoding="utf-8", newline="\n")
        print(
            f"{'Validated' if args.check else 'Built'} runtime profile: {len(content):,} bytes; {len(profile['bullet_bank'])} bullets; prohibited client references: 0."
        )
        return 0
    except RuntimeProfileError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        print(
            "Error: invalid source/profile structure or file access; no private content displayed.",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
