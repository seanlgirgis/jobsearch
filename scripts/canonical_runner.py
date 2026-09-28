"""Canonical runner: local gate, cached analysis, explicit generation and application record."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
import yaml
from jsonschema.exceptions import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.build_runtime_profile import (  # noqa: E402
    PROFILE_PATH,
    REPORT_PATH,
    RuntimeProfileError,
    build_profile,
    canonical,
    digest,
)
from src.ai.llm_client import LLMClient  # noqa: E402
from src.ai.model_profiles import ProfileError  # noqa: E402
from src.pipeline.artifacts import (  # noqa: E402
    prepare_artifacts,
    public_text_check,
    validate_package,
    verify_artifacts,
)
from src.pipeline.contracts import (  # noqa: E402
    ANALYSIS_PROMPT,
    ANALYSIS_SCHEMA,
    PACKAGE_PROMPT,
    PROMPT_VERSION,
    package_schema,
)
from src.pipeline.local_gate import job_hash, local_gate, paid_job_text  # noqa: E402
from src.pipeline.storage import (  # noqa: E402
    PipelineError,
    atomic_text,
    cached_call,
    workspace_lock,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]


def verified_profile(root):
    profile, report = build_profile(root, root.parent / "Grok_DIRECTOR")
    content = canonical(profile) + b"\n"
    if (root / PROFILE_PATH).read_bytes() != content or (root / REPORT_PATH).read_text(
        encoding="utf-8"
    ) != report:
        raise PipelineError(
            "Runtime profile/report is stale; review sources and run build_runtime_profile.py."
        )
    return profile, digest(content)


def load_metadata(folder):
    path = folder / "metadata.yaml"
    if not path.exists():
        return {}
    value = yaml.safe_load(path.read_text(encoding="utf-8-sig")) or {}
    if not isinstance(value, dict):
        raise PipelineError("Invalid existing job metadata.")
    return value


def save_metadata(folder, metadata, state):
    metadata["last_runner_state"] = state
    metadata["status"] = (
        "ASSUMED_APPLIED" if metadata.get("application", {}).get("applied") else state
    )
    atomic_text(
        folder / "metadata.yaml", yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True)
    )


def canonical_client(root, profile_name, stage, factory):
    client = (
        factory(profile_name)
        if factory
        else LLMClient(profile_name, config_dir=root / "config", env_file=root / ".env")
    )
    profile = client.profile
    if client.profile_name != profile_name or profile.fallbacks:
        raise PipelineError(
            "Canonical stages require their named profile and an empty fallback list."
        )
    if (
        profile.primary.model is None
        or not profile.primary.supports_json_schema
        or profile.structured_output == "off"
    ):
        raise PipelineError("Configure a schema-capable primary model ID for this stage first.")
    if stage == "generation" and not profile.allow_artifacts:
        raise PipelineError("The selected generation profile disallows artifact generation.")
    return client


def stage_call(
    root, stage, profile_name, text, profile, profile_hash, *, factory, analysis=None, cover=False
):
    client = canonical_client(root, profile_name, stage, factory)
    payload = {"job": paid_job_text(text), "profile": profile}
    if analysis is not None:
        payload.update(analysis=analysis, cover_requested=cover)
    schema = ANALYSIS_SCHEMA if stage == "analysis" else package_schema(profile)
    messages = [
        {"role": "system", "content": ANALYSIS_PROMPT if stage == "analysis" else PACKAGE_PROMPT},
        {"role": "user", "content": canonical(payload).decode("utf-8")},
    ]
    identity = {
        "job_hash": job_hash(text),
        "runtime_profile_hash": profile_hash,
        "prompt_version": PROMPT_VERSION,
        "model_profile": profile_name,
        "pipeline_stage": stage,
        "model_settings": client.profile.model_dump(mode="json"),
        "schema_sha256": digest(canonical(schema)),
        "request_sha256": digest(canonical(messages)),
    }
    if analysis is not None:
        identity.update(analysis_sha256=digest(canonical(analysis)), cover_requested=cover)
    validator = (
        public_text_check
        if stage == "analysis"
        else lambda value: validate_package(value, profile, cover)
    )
    return cached_call(
        root,
        identity,
        client,
        messages,
        schema,
        "job_analysis" if stage == "analysis" else "job_package",
        validator,
    )


def record_application(folder, metadata, method, applied_date, notes):
    artifacts = metadata.get("artifacts")
    if not artifacts:
        raise PipelineError(
            "No completed generated package for this job; generate and review it first."
        )
    verify_artifacts(folder, artifacts)
    application = metadata.get("application", {})
    entry = {"date": applied_date, "status": "Applied", "method": method, "notes": notes or ""}
    history = list(application.get("history", []))
    if entry not in history:
        history.append(entry)
    metadata["application"] = {
        **application,
        "applied": True,
        "applied_date": applied_date,
        "applied_method": method,
        "application_notes": notes or "",
        "history": history,
    }
    save_metadata(folder, metadata, "ASSUMED_APPLIED")
    write_json(folder / "application.json", metadata["application"])


def continuation_command(
    path,
    state,
    *,
    override_duplicate,
    override_suitability,
    reason,
    cover,
    analysis_profile,
    generation_profile,
):
    """One syntactically valid PowerShell command; at most one -Reason; keep -Cover."""
    quoted_path = "'" + str(path).replace("'", "''") + "'"
    if state == "READY_TO_APPLY":
        return (
            f".\\job-runner.ps1 {quoted_path} -Mode apply -AssumeApplied "
            "-Method '<actual method>' -Date '<YYYY-MM-DD>' -Notes '<submission details>'"
        )
    if state not in {"TIER0_CLEAR", "TIER0_OVERRIDDEN", "TRIAGED", "AWAITING_DECISION"}:
        return None
    target_mode = "triage" if state.startswith("TIER0") else "generate"
    parts = [f".\\job-runner.ps1 {quoted_path}", f"-Mode {target_mode}"]
    parts.append("-AnalysisProfile '" + analysis_profile.replace("'", "''") + "'")
    if target_mode == "generate":
        parts.append("-GenerationProfile '" + generation_profile.replace("'", "''") + "'")
    if cover:
        parts.append("-Cover")
    if override_duplicate:
        parts.append("-OverrideDuplicate")
    need_suitability = bool(override_suitability) or state == "AWAITING_DECISION"
    if need_suitability:
        parts.append("-OverrideSuitability")
    if override_duplicate or need_suitability:
        reason_text = (reason or "").strip() or "<actual authorized reason>"
        parts.append("-Reason '" + reason_text.replace("'", "''") + "'")
    return " ".join(parts)


def failure_handoff(folder, metadata, cache_results):
    return {
        "state": "FAILED",
        "folder": str(folder),
        "tier0_decision": metadata.get("tier0_decision"),
        "llm_decision": metadata.get("llm_decision"),
        "user_decision": metadata.get("user_decision"),
        "resume": None,
        "cover": None,
        "cache": cache_results,
        "next_command": None,
        "cost": {
            "actual_usd": None,
            "note": "Dollar usage is not collected; Cline usage is separate.",
            "max_new_provider_requests": sum(
                x.get("result") == "MISS" for x in cache_results.values()
            ),
        },
    }


def usage_report(cache_results):
    """Separate provider-reported spend for this command from cached historical usage."""
    fields = (
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "reasoning_tokens",
        "actual_usd",
    )
    totals = {field: 0 for field in fields}
    known = {field: False for field in fields}
    stages = {}
    for stage, details in cache_results.items():
        usage = details.get("usage")
        source = "new_provider_call" if details.get("result") == "MISS" else "cache"
        stages[stage] = {"source": source, "usage": usage}
        if source != "new_provider_call" or not isinstance(usage, dict):
            continue
        for field in fields:
            value = usage.get(field)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                totals[field] += value
                known[field] = True
    this_run = {
        "provider_requests": sum(
            details.get("result") == "MISS" for details in cache_results.values()
        ),
        **{field: totals[field] if known[field] else None for field in fields},
    }
    return {"this_run": this_run, "by_stage": stages}


def human_summary(result):
    """Readable terminal handoff; full machine-readable JSON remains on stdout."""
    lines = [f"Job runner: {result['state']}"]
    highlights = result.get("highlights")
    if highlights:
        role = " — ".join(
            value for value in (highlights.get("company"), highlights.get("role")) if value
        )
        if role:
            lines.append(f"Role: {role}")
        score = highlights.get("score")
        recommendation = highlights.get("recommendation")
        if score is not None or recommendation:
            details = ["score unavailable"] if score is None else []
            if score is not None:
                details.append(f"score {score}/100")
            if recommendation:
                details.append(f"recommendation {recommendation}")
            lines.append("Fit: " + "; ".join(details))
        for key, label in (("strengths", "Strengths"), ("gaps", "Gaps")):
            values = highlights.get(key) or []
            if values:
                lines.append(f"{label}: " + "; ".join(values[:3]))
    usage = result.get("usage", {}).get("this_run", {})
    calls = usage.get("provider_requests", 0)
    if calls == 0:
        lines.append("Usage this run: no new provider call (local work or cached result).")
    else:
        parts = [f"{calls} provider call(s)"]
        if usage.get("total_tokens") is not None:
            parts.append(f"{usage['total_tokens']} tokens")
        if usage.get("actual_usd") is not None:
            parts.append(f"${usage['actual_usd']:.6f}")
        else:
            parts.append("provider did not report dollar usage")
        lines.append("Usage this run: " + ", ".join(parts) + ".")
    if result.get("resume"):
        lines.append(f"Resume: {result['resume']}")
    if result.get("cover"):
        lines.append(f"Cover: {result['cover']}")
    if result.get("next_command"):
        lines.append("Next: " + result["next_command"])
    return "\n".join(lines)


def report_analysis(folder, packet):
    analysis = packet["analysis"]
    score = "unavailable" if analysis["score"] is None else f"{analysis['score']}/100"
    lines = [
        "# LLM gate report",
        "",
        f"Score: {score}",
        f"Recommendation: {analysis['recommendation']}",
        "",
        analysis["fit_rationale"],
    ]
    for key, title in (
        ("strengths", "Strengths"),
        ("gaps", "Gaps"),
        ("keywords", "Keywords"),
        ("tailoring_plan", "Tailoring plan"),
    ):
        lines += ["", f"## {title}", "", *[f"- {value}" for value in analysis[key]]]
    lines += ["", "User decision: " + json.dumps(packet["user_decision"]), ""]
    atomic_text(folder / "score/llm_gate_report.md", "\n".join(lines))
    write_json(folder / "tailored/job_packet.json", packet)


def run(
    root,
    intake,
    mode,
    *,
    override_duplicate=False,
    override_suitability=False,
    reason=None,
    cover=False,
    assume_applied=False,
    method=None,
    applied_date=None,
    notes=None,
    analysis_profile="economy",
    generation_profile="quality",
    client_factory=None,
    semantic=None,
):
    root = Path(root).resolve()
    if mode not in {"gate", "triage", "generate", "apply"}:
        raise PipelineError("Unknown runner mode.")
    reason = reason.strip() if isinstance(reason, str) else None
    if (override_duplicate or override_suitability) and not reason:
        raise PipelineError("Each override requires a nonblank --reason.")
    if assume_applied:
        if mode not in {"generate", "apply"} or not method or not method.strip():
            raise PipelineError("Application recording requires generate/apply mode and --method.")
        if not applied_date or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", applied_date):
            raise PipelineError("Application date must be YYYY-MM-DD.")
        try:
            date.fromisoformat(applied_date)
        except ValueError:
            raise PipelineError("Application date is not a valid calendar date.") from None
    elif mode == "apply" or any(value is not None for value in (method, applied_date, notes)):
        raise PipelineError("Application fields and apply mode require explicit --assume-applied.")
    if mode == "apply" and (cover or override_duplicate or override_suitability):
        raise PipelineError(
            "Apply-only uses the completed package; omit cover and override switches."
        )
    path = Path(intake)
    path = path if path.is_absolute() else root / path
    text = path.read_text(encoding="utf-8-sig").strip()
    if not text or len(text.encode("utf-8")) > 40000:
        raise PipelineError("Provide a nonempty intake of at most 40,000 UTF-8 bytes.")
    key = job_hash(text)
    folder = root / "data/jobs" / f"runner_{key[:8]}"
    cache_results = {}
    analysis = None
    with workspace_lock(root):
        metadata = load_metadata(folder)
        if folder.exists():
            if not metadata.get("canonical_runner") or metadata.get("job_hash") != key:
                raise PipelineError(
                    "Existing folder is not this canonical job or has a hash collision; nothing overwritten."
                )
            raw = folder / "raw/job_description.md"
            if not raw.exists() or job_hash(raw.read_text(encoding="utf-8-sig")) != key:
                raise PipelineError(
                    "Existing intake evidence is missing or changed; nothing overwritten."
                )
        if mode == "apply":
            record_application(folder, metadata, method.strip(), applied_date, notes)
            state = "ASSUMED_APPLIED"
        else:
            gate = (
                local_gate(root, text, folder)
                if semantic is None
                else local_gate(root, text, folder, semantic=semantic)
            )
            gate["duplicate_override"] = {"reason": reason} if override_duplicate else None
            folder.mkdir(parents=True, exist_ok=True)
            if not (folder / "raw/job_description.md").exists():
                atomic_text(folder / "raw/job_description.md", text + "\n")
            metadata.update(
                job_id=folder.name,
                job_hash=key,
                canonical_runner=True,
                tier0_decision=gate["tier0_decision"],
            )
            write_json(folder / "score/local_gate.json", gate)
            if override_duplicate:
                event = {"type": "duplicate_override", "reason": reason}
                history = metadata.setdefault("decision_history", [])
                if event not in history:
                    history.append(event)
            blocked = bool(gate["eligibility_blocks"]) or (
                gate["duplicate_or_check_blocked"] and not override_duplicate
            )
            if blocked:
                save_metadata(folder, metadata, "BLOCKED")
                state = "BLOCKED"
            elif mode == "gate":
                save_metadata(
                    folder, metadata, "TIER0_OVERRIDDEN" if override_duplicate else "TIER0_CLEAR"
                )
                state = metadata["last_runner_state"]
            else:
                save_metadata(folder, metadata, "ANALYZING")
                try:
                    profile, profile_hash = verified_profile(root)
                    analysis, tier1 = stage_call(
                        root,
                        "analysis",
                        analysis_profile,
                        text,
                        profile,
                        profile_hash,
                        factory=client_factory,
                    )
                    cache_results["tier1"] = tier1
                    decision = metadata.get("user_decision")
                    if decision and decision.get("analysis_cache_key") != tier1["key"]:
                        decision = None
                    if mode == "generate":
                        decision = {
                            "decision": (
                                "ACCEPTED"
                                if analysis["recommendation"] == "PROCEED" or override_suitability
                                else "GENERATE_REQUESTED"
                            ),
                            "source": "generate_command",
                            "reason": reason,
                            "suitability_override": override_suitability,
                            "analysis_cache_key": tier1["key"],
                        }
                        history = metadata.setdefault("decision_history", [])
                        if decision not in history:
                            history.append(decision)
                    metadata.update(
                        llm_decision=analysis["recommendation"],
                        user_decision=decision,
                        company=analysis["company"],
                        role=analysis["title"],
                        score=analysis["score"],
                    )
                    packet = {
                        "analysis": analysis,
                        "provenance": tier1,
                        "tier0_decision": gate["tier0_decision"],
                        "llm_decision": analysis["recommendation"],
                        "user_decision": decision,
                        "duplicate_override": gate["duplicate_override"],
                    }
                    report_analysis(folder, packet)
                    state = "TRIAGED" if mode == "triage" else "AWAITING_DECISION"
                    save_metadata(folder, metadata, state)
                    if mode == "generate" and decision["decision"] == "ACCEPTED":
                        save_metadata(folder, metadata, "GENERATING")
                        package, tier2 = stage_call(
                            root,
                            "generation",
                            generation_profile,
                            text,
                            profile,
                            profile_hash,
                            factory=client_factory,
                            analysis=analysis,
                            cover=cover,
                        )
                        metadata["artifacts"] = prepare_artifacts(
                            root,
                            folder,
                            package,
                            profile,
                            profile_hash,
                            {"tier1": tier1, "tier2": tier2},
                        )
                        cache_results["tier2"] = tier2
                        state = "READY_TO_APPLY"
                        save_metadata(folder, metadata, state)
                        if assume_applied:
                            record_application(
                                folder, metadata, method.strip(), applied_date, notes
                            )
                            state = "ASSUMED_APPLIED"
                except Exception:
                    save_metadata(folder, metadata, "FAILED")
                    write_json(
                        folder / "runner_result.json",
                        failure_handoff(folder, metadata, cache_results),
                    )
                    raise
        artifacts = (
            metadata.get("artifacts") if state in {"READY_TO_APPLY", "ASSUMED_APPLIED"} else None
        )
        next_command = continuation_command(
            path,
            state,
            override_duplicate=override_duplicate,
            override_suitability=override_suitability,
            reason=reason,
            cover=cover,
            analysis_profile=analysis_profile,
            generation_profile=generation_profile,
        )
        result = {
            "state": state,
            "folder": str(folder),
            "tier0_decision": metadata.get("tier0_decision"),
            "llm_decision": metadata.get("llm_decision"),
            "user_decision": metadata.get("user_decision"),
            "resume": str(folder / artifacts["resume"]) if artifacts else None,
            "cover": (
                str(folder / artifacts["cover"]) if artifacts and artifacts.get("cover") else None
            ),
            "cache": cache_results,
            "highlights": (
                {
                    "company": analysis["company"],
                    "role": analysis["title"],
                    "score": analysis["score"],
                    "recommendation": analysis["recommendation"],
                    "strengths": analysis["strengths"],
                    "gaps": analysis["gaps"],
                }
                if analysis is not None
                else None
            ),
            "profiles": {
                "analysis": analysis_profile,
                "generation": generation_profile if mode == "generate" else None,
            },
            "next_command": next_command,
            "cost": {
                "actual_usd": usage_report(cache_results)["this_run"]["actual_usd"],
                "note": "Only provider-reported usage is shown; Cline usage is separate.",
                "max_new_provider_requests": usage_report(cache_results)["this_run"][
                    "provider_requests"
                ],
            },
            "usage": usage_report(cache_results),
        }
        write_json(folder / "runner_result.json", result)
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intake")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "-Mode", "--mode", choices=["gate", "triage", "generate", "apply"], default="triage"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Local gate only; writes gate records but never calls providers",
    )
    parser.add_argument("--override-duplicate", action="store_true")
    parser.add_argument("--override-suitability", action="store_true")
    parser.add_argument("--reason")
    parser.add_argument("--cover", action="store_true")
    parser.add_argument(
        "--analysis-profile",
        default="economy",
        help="Named schema-capable profile for analysis (default: economy).",
    )
    parser.add_argument(
        "--generation-profile",
        default="quality",
        help="Named schema-capable artifact profile for generation (default: quality).",
    )
    parser.add_argument("--assume-applied", action="store_true")
    parser.add_argument("--method")
    parser.add_argument("--date", dest="applied_date")
    parser.add_argument("--notes")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the full machine-readable result after the normal human summary.",
    )
    args = parser.parse_args(argv)
    try:
        result = run(
            args.root,
            args.intake,
            "gate" if args.dry_run else args.mode,
            override_duplicate=args.override_duplicate,
            override_suitability=args.override_suitability,
            reason=args.reason,
            cover=args.cover,
            assume_applied=args.assume_applied,
            method=args.method,
            applied_date=args.applied_date,
            notes=args.notes,
            analysis_profile=args.analysis_profile,
            generation_profile=args.generation_profile,
        )
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(human_summary(result))
        return 1 if result["state"] in {"BLOCKED", "AWAITING_DECISION"} else 0
    except (PipelineError, ProfileError, RuntimeProfileError) as error:
        print(f"Error: {error}", file=sys.stderr)
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
        yaml.YAMLError,
        ValidationError,
    ):
        print(
            "Error: missing, malformed, or inaccessible local input/artifact; no raw content displayed.",
            file=sys.stderr,
        )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
