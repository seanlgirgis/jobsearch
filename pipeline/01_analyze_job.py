"""Minimal Tier 1 analyzer: single LLM call to produce job_packet.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ai.grok_client import GrokClient
from utils.metadata_io import load_metadata, save_metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Tier 1 LLM job analysis.")
    parser.add_argument("--job-id", required=True, help="Job folder id, e.g. 00066_213afca5")
    parser.add_argument("--model", default="grok-3", help="Grok model")
    parser.add_argument("--temperature", type=float, default=0.0, help="LLM temperature")
    return parser.parse_args()


def _extract_json_object(raw: str) -> Dict[str, Any]:
    text = raw.strip()
    candidates = [text]

    if text.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        stripped = re.sub(r"\s*```$", "", stripped)
        candidates.append(stripped)

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(text[start : end + 1])

    for candidate in candidates:
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            continue

    raise ValueError("Could not extract valid JSON object from LLM response")


def _short_error_message(exc: Exception, max_len: int = 220) -> str:
    message = f"{exc.__class__.__name__}: {str(exc).strip()}"
    if len(message) <= max_len:
        return message
    return message[: max_len - 3] + "..."


def _build_candidate_context(source: Dict[str, Any]) -> Dict[str, Any]:
    personal = source.get("personal_info", {})
    summary = source.get("professional_summary", {})
    skills = source.get("skills", [])
    experiences = source.get("experiences", [])

    top_skills = []
    for skill in skills[:20]:
        if isinstance(skill, dict) and skill.get("name"):
            top_skills.append(str(skill["name"]))

    recent_experience = []
    for exp in experiences[:3]:
        if not isinstance(exp, dict):
            continue
        recent_experience.append(
            {
                "company": exp.get("company", ""),
                "role": exp.get("role", ""),
                "highlights": (exp.get("highlights", []) or [])[:2],
            }
        )

    return {
        "preferred_title": personal.get("preferred_title", ""),
        "target_roles": personal.get("target_roles", []),
        "location_preference": personal.get("location_preference", ""),
        "work_authorization": personal.get("work_authorization", ""),
        "summary_short": summary.get("short", ""),
        "top_skills": top_skills,
        "recent_experience": recent_experience,
    }


def _build_prompt(
    job_id: str,
    job_hash: str,
    raw_job_text: str,
    candidate_context: Dict[str, Any],
) -> str:
    schema_hint = {
        "artifact_type": "job_packet",
        "artifact_schema_version": "v1",
        "job_id": job_id,
        "job_hash": job_hash,
        "score": 0,
        "llm_decision": "proceed",
        "rationale": "",
        "job_facts": {
            "title": "",
            "company": "",
            "location": "",
            "employment_type": "",
        },
        "requirements": {
            "must_have_skills": [],
            "nice_to_have_skills": [],
            "responsibilities": [],
            "requirements_text": [],
            "ats_keywords": [],
            "missing_skills": [],
            "risk_flags": [],
        },
        "tailoring_plan": {
            "positioning_angle": "",
            "priority_experiences": [],
            "priority_keywords": [],
            "bullet_strategy": [],
        },
    }

    return (
        "You are a strict JSON generator for job analysis.\n"
        "Return JSON only. No markdown, no code fences, no extra text.\n"
        "Be concise and grounded in the provided inputs.\n"
        "Do not invent candidate experience beyond the provided context.\n"
        "Use empty arrays when unknown.\n\n"
        "Analyze the job and candidate context in one pass and return exactly one JSON object.\n"
        f"Required output shape example:\n{json.dumps(schema_hint, indent=2)}\n\n"
        "Constraints:\n"
        "- Set artifact_type='job_packet' and artifact_schema_version='v1'.\n"
        f"- Set job_id='{job_id}' and job_hash='{job_hash}'.\n"
        "- score is integer 0-100.\n"
        "- llm_decision must be one of: proceed, hold, skip.\n"
        "- rationale must be short and grounded.\n\n"
        f"Candidate context JSON:\n{json.dumps(candidate_context, indent=2)}\n\n"
        f"Raw job text:\n{raw_job_text}"
    )


def main() -> None:
    args = parse_args()

    job_dir = Path("data/jobs") / args.job_id
    metadata_path = job_dir / "metadata.yaml"
    local_gate_path = job_dir / "score" / "local_gate.json"
    raw_intake_path = job_dir / "raw" / "raw_intake.md"

    metadata = load_metadata(metadata_path)
    local_gate = json.loads(local_gate_path.read_text(encoding="utf-8"))
    raw_job_text = raw_intake_path.read_text(encoding="utf-8")

    tier0_decision = metadata.get("tier0_decision")
    if tier0_decision == "reject_early":
        print("=== ANALYZE JOB ===")
        print(f"Job ID: {args.job_id}")
        print("Tier0 Decision: reject_early")
        print("Result: refusing to run LLM analysis")
        return

    job_packet_path = job_dir / "tailored" / "job_packet.json"
    has_cached_packet = job_packet_path.is_file()
    has_complete_metadata = (
        metadata.get("llm_decision") is not None
        and metadata.get("score") is not None
    )
    if has_cached_packet and has_complete_metadata:
        print("=== ANALYZE JOB ===")
        print(f"Job ID: {args.job_id}")
        print("Result: cached analysis found, skipping LLM call")
        print(f"Artifact: data/jobs/{args.job_id}/tailored/job_packet.json")
        return

    source_of_truth_path = Path("data/source_of_truth.json")
    source_of_truth = json.loads(source_of_truth_path.read_text(encoding="utf-8"))
    candidate_context = _build_candidate_context(source_of_truth)
    candidate_context_text = json.dumps(candidate_context, indent=2)

    prompt_text = _build_prompt(
        job_id=args.job_id,
        job_hash=str(local_gate.get("job_hash", metadata.get("job_hash", ""))),
        raw_job_text=raw_job_text,
        candidate_context=candidate_context,
    )
    debug_dir = job_dir / "debug"
    timestamp = datetime.now().isoformat()

    print("=== LLM REQUEST DEBUG ===")
    print(f"Job ID: {args.job_id}")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"Normalized Text Length: {len(raw_job_text)}")
    print(f"Context Length: {len(candidate_context_text)}")
    print(f"Prompt Size (chars): {len(prompt_text)}")
    print("USING LEGACY GROK CALL STRUCTURE")

    try:
        grok = GrokClient(model=args.model)
        response = grok.chat(
            messages=[{"role": "user", "content": prompt_text}],
            temperature=args.temperature,
            max_tokens=4000,
        )
        print(f"LLM Response Length: {len(response)}")
        if not response or not response.strip():
            raise ValueError("LLM returned an empty response")
    except Exception as exc:
        debug_dir.mkdir(parents=True, exist_ok=True)
        failure_dump_path = debug_dir / "llm_failure_dump.txt"
        failure_dump_path.write_text(
            "\n".join(
                [
                    f"timestamp: {timestamp}",
                    f"error: {_short_error_message(exc, max_len=2000)}",
                    "",
                    "prompt_preview_first_5000_chars:",
                    prompt_text[:5000],
                ]
            ),
            encoding="utf-8",
        )

        error_message = _short_error_message(exc)
        metadata["last_llm_error"] = error_message
        metadata["last_llm_attempt_at"] = datetime.now().isoformat()
        save_metadata(metadata_path, metadata)

        print("=== ANALYZE JOB ===")
        print(f"Job ID: {args.job_id}")
        print("Tier0 Decision: needs_llm")
        print("Result: LLM analysis failed")
        print(f"Error: {error_message}")
        print("Metadata updated with retry info")
        print("=== LLM DEBUG INFO ===")
        print("Failure Type: API_ERROR")
        print(f"Dump File: data/jobs/{args.job_id}/debug/llm_failure_dump.txt")
        return

    try:
        packet = _extract_json_object(response)
    except Exception as exc:
        debug_dir.mkdir(parents=True, exist_ok=True)
        bad_json_path = debug_dir / "llm_bad_json.txt"
        bad_json_path.write_text(
            "\n".join(
                [
                    f"timestamp: {timestamp}",
                    f"parse_error: {_short_error_message(exc, max_len=2000)}",
                    "",
                    "raw_response:",
                    response,
                ]
            ),
            encoding="utf-8",
        )

        error_message = _short_error_message(exc)
        metadata["last_llm_error"] = error_message
        metadata["last_llm_attempt_at"] = datetime.now().isoformat()
        save_metadata(metadata_path, metadata)

        print("=== ANALYZE JOB ===")
        print(f"Job ID: {args.job_id}")
        print("Tier0 Decision: needs_llm")
        print("Result: LLM analysis failed")
        print(f"Error: {error_message}")
        print("Metadata updated with retry info")
        print("=== LLM DEBUG INFO ===")
        print("Failure Type: BAD_JSON")
        print(f"Dump File: data/jobs/{args.job_id}/debug/llm_bad_json.txt")
        return

    tailored_dir = job_dir / "tailored"
    tailored_dir.mkdir(parents=True, exist_ok=True)
    job_packet_path = tailored_dir / "job_packet.json"
    job_packet_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")

    metadata["llm_decision"] = packet.get("llm_decision")
    metadata["score"] = packet.get("score")
    if "last_llm_error" in metadata:
        metadata["last_llm_error"] = None
    if "last_llm_attempt_at" in metadata:
        metadata["last_llm_attempt_at"] = None
    save_metadata(metadata_path, metadata)

    print("=== ANALYZE JOB ===")
    print(f"Job ID: {args.job_id}")
    print("Tier0 Decision: needs_llm")
    print(f"LLM Decision: {packet.get('llm_decision')}")
    print(f"Score: {packet.get('score')}")
    print(f"Artifact: data/jobs/{args.job_id}/tailored/job_packet.json")


if __name__ == "__main__":
    main()
