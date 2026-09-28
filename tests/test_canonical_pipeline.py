"""Offline cutover: real gate/cache/client/schema/render code; mocked HTTP and embedding boundary."""

from __future__ import annotations

import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import httpx
from docx import Document
from jsonschema import validate
from openai import OpenAI

from scripts import canonical_runner as runner
from scripts.build_runtime_profile import (
    REQUIRED,
    PROFILE_PATH,
    REPORT_PATH,
    build_profile,
    canonical,
)
from src.ai.llm_client import LLMClient
from src.pipeline.contracts import ANALYSIS_SCHEMA
from src.pipeline.local_gate import job_hash, paid_job_text, semantic_worker
from src.pipeline.storage import PipelineError, read_json, write_json, workspace_lock

REPO = Path(__file__).resolve().parents[1]
JOB = "Example Systems seeks a senior capacity engineer to build Python and SQL reporting, analyze infrastructure utilization, improve observability and forecast demand."


class CanonicalPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "jobsearch"
        self.root.mkdir()
        for relative in REQUIRED.values():
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, target)
        for name in (
            "05_render_resume.py",
            "08_render_cover_letter.py",
            "quality_check.py",
        ):
            target = self.root / "scripts" / name
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(REPO / "scripts" / name, target)
        shutil.copyfile(
            REPO / "config/model_profiles.example.json",
            self.root / "config/model_profiles.example.json",
        )
        self.profile, report = build_profile(
            self.root, self.root.parent / "Grok_DIRECTOR"
        )
        (self.root / PROFILE_PATH).write_bytes(canonical(self.profile) + b"\n")
        (self.root / REPORT_PATH).write_text(report, encoding="utf-8")
        self.intake = self.root / "intake.md"
        self.intake.write_text(JOB, encoding="utf-8")
        self.configure()
        self.analysis = {
            "company": "Example Systems",
            "title": "Capacity Engineer",
            "location": None,
            "score": 88,
            "fit_rationale": "Strong capacity and automation alignment.",
            "strengths": ["Python and infrastructure reporting"],
            "gaps": ["Confirm engagement schedule"],
            "recommendation": "PROCEED",
            "keywords": ["Python", "capacity"],
            "tailoring_plan": [
                "Emphasize capacity forecasting and current reporting work"
            ],
        }
        self.package = {
            "resume": {
                "summary": "Capacity and performance engineer with Python automation and practical workflow engineering experience. Background includes infrastructure reporting, forecasting and observability across enterprise environments. Applies established engineering skills to improve data quality and support clearer operational decisions, with practical AI workflows and knowledge-base research grounded in capacity and performance work.",
                "skill_names": ["Python", "Capacity Planning / Forecasting"],
                "experience": [
                    {
                        "evidence_id": "current",
                        "bullet_ids": ["current_reporting", "current_research"],
                    },
                    {"evidence_id": "citi", "bullet_ids": ["citi_etl"]},
                ],
                "projects": [],
            },
            "cover": {
                "intro": "I am interested in the capacity engineering opportunity with Example Systems. My background combines infrastructure capacity planning, performance analysis and Python automation, with a practical focus on making operational reporting clearer and more useful.",
                "body": [
                    "My experience includes building telemetry pipelines and supporting capacity reporting and forecasting. I also bring observability experience and an interest in practical AI workflows. These areas align with the role's emphasis on infrastructure utilization, data quality and reporting, and I would welcome the opportunity to discuss how that experience could support your team."
                ],
                "conclusion": "Thank you for considering my application. I would appreciate a conversation about the team's priorities and the scope of this role.",
            },
        }
        self.requests = []
        self.status = 200
        self.semantic_calls = 0
        self.guard = patch(
            "socket.socket.connect", side_effect=AssertionError("Network prohibited")
        )
        self.guard.start()
        self.addCleanup(self.guard.stop)
        self.dotenv_guard = patch(
            "src.ai.llm_client.load_dotenv",
            side_effect=AssertionError("Real keys prohibited"),
        )
        self.dotenv_guard.start()
        self.addCleanup(self.dotenv_guard.stop)

    def configure(
        self,
        *,
        economy="test-economy",
        quality="test-quality",
        fallback=False,
        artifacts=True,
    ):
        write_json(
            self.root / "config/model_profiles.local.json",
            {
                "profiles": {
                    "economy": {
                        "primary": {
                            "provider": "openrouter",
                            "model": economy,
                            "supports_json_schema": True,
                        },
                        "fallbacks": (
                            [
                                {
                                    "provider": "xai",
                                    "model": "test-fallback",
                                    "supports_json_schema": True,
                                }
                            ]
                            if fallback
                            else []
                        ),
                    },
                    "quality": {
                        "primary": {
                            "provider": "openrouter",
                            "model": quality,
                            "supports_json_schema": True,
                        },
                        "allow_artifacts": artifacts,
                    },
                }
            },
        )

    def http_handler(self, request):
        body = json.loads(request.content)
        self.requests.append(body)
        if self.status != 200:
            return httpx.Response(
                self.status, json={"error": {"message": "synthetic provider failure"}}
            )
        if "response_format" in body:
            name = body["response_format"]["json_schema"]["name"]
        else:
            payload = json.loads(body["messages"][1]["content"])
            name = "job_package" if "analysis" in payload else "job_analysis"
        value = copy.deepcopy(self.analysis if name == "job_analysis" else self.package)
        if name == "job_package":
            payload = json.loads(body["messages"][1]["content"])
            if not payload.get("cover_requested"):
                value["cover"] = None
        return httpx.Response(
            200,
            json={
                "id": "synthetic-completion",
                "object": "chat.completion",
                "created": 0,
                "model": body["model"],
                "choices": [
                    {
                        "index": 0,
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": json.dumps(value),
                            "refusal": None,
                        },
                    }
                ],
                "usage": {
                    "prompt_tokens": 101,
                    "completion_tokens": 29,
                    "total_tokens": 130,
                    "cost": 0.000123,
                    "completion_tokens_details": {"reasoning_tokens": 11},
                },
            },
        )

    def factory(self, name):
        def sdk_factory(**kwargs):
            self.assertEqual(kwargs["max_retries"], 0)
            self.assertEqual(kwargs["api_key"], "synthetic-test-key")
            return OpenAI(
                http_client=httpx.Client(
                    transport=httpx.MockTransport(self.http_handler)
                ),
                **kwargs,
            )

        return LLMClient(
            name,
            config_dir=self.root / "config",
            environ={"OPENROUTER_API_KEY": "synthetic-test-key"},
            client_factory=sdk_factory,
        )

    def semantic(self, root, text, own):
        self.semantic_calls += 1
        return {
            "status": "CLEAR",
            "matches": [],
            "reason": "Synthetic local embedding boundary",
        }

    def run_job(self, mode="triage", **kwargs):
        with redirect_stdout(io.StringIO()):
            return runner.run(
                self.root,
                self.intake,
                mode,
                client_factory=self.factory,
                semantic=kwargs.pop("semantic", self.semantic),
                **kwargs,
            )

    def meta(self, result):
        return runner.load_metadata(Path(result["folder"]))

    def historical_job(self, text=JOB, collection="applied_jobs"):
        folder = self.root / "data" / collection / "00001_historical"
        (folder / "raw").mkdir(parents=True)
        (folder / "raw/job_description.md").write_text(text, encoding="utf-8")
        (folder / "metadata.yaml").write_text(
            "company: Example Systems\napplication:\n  applied: true\n",
            encoding="utf-8",
        )
        return folder

    def test_exact_duplicate_stops_before_tier1(self):
        old = self.historical_job(" \n " + JOB.upper().replace(" ", "  ") + "\n")
        before = (old / "metadata.yaml").read_bytes()
        result = self.run_job()
        self.assertEqual(result["state"], "BLOCKED")
        self.assertEqual(self.requests, [])
        self.assertEqual(self.semantic_calls, 0)
        self.assertEqual(before, (old / "metadata.yaml").read_bytes())

    def test_duplicate_override_is_recorded_and_continues(self):
        self.historical_job()
        result = self.run_job(
            override_duplicate=True, reason="Verified new requisition"
        )
        self.assertEqual(result["state"], "TRIAGED")
        self.assertEqual(len(self.requests), 1)
        gate = read_json(Path(result["folder"]) / "score/local_gate.json")
        self.assertEqual(gate["tier0_decision"], "DUPLICATE")
        self.assertEqual(
            gate["duplicate_override"]["reason"], "Verified new requisition"
        )
        self.assertIn(
            {"type": "duplicate_override", "reason": "Verified new requisition"},
            self.meta(result)["decision_history"],
        )

    def test_semantic_duplicate_and_missing_index_block(self):
        for state in ("DUPLICATE", "BLOCKED"):
            result = self.run_job(
                semantic=lambda *a: {
                    "status": state,
                    "matches": [],
                    "reason": "fixture",
                }
            )
            self.assertEqual(result["state"], "BLOCKED")
        self.assertEqual(self.requests, [])

    def test_eligibility_blocks_even_with_duplicate_override(self):
        self.intake.write_text(JOB + " This job is closed.", encoding="utf-8")
        for mode in ("gate", "triage", "generate"):
            result = self.run_job(
                mode, override_duplicate=True, reason="A new requisition"
            )
            self.assertEqual(result["state"], "BLOCKED")
        self.assertEqual(self.requests, [])

    def test_short_intake_blocks(self):
        self.intake.write_text("Too short", encoding="utf-8")
        self.assertEqual(self.run_job()["state"], "BLOCKED")
        self.assertEqual(self.requests, [])

    def test_both_overrides_require_nonblank_reasons_before_writes(self):
        for option in ("override_duplicate", "override_suitability"):
            for reason in (None, "", "   "):
                with self.assertRaises(PipelineError):
                    self.run_job(**{option: True, "reason": reason})
        self.assertFalse((self.root / "data/jobs").exists())
        self.assertEqual(self.requests, [])

    def test_triage_uses_one_real_cached_schema_call_and_stops(self):
        result = self.run_job()
        self.assertEqual(result["state"], "TRIAGED")
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(self.requests[0]["model"], "test-economy")
        packet = read_json(Path(result["folder"]) / "tailored/job_packet.json")
        validate(packet["analysis"], ANALYSIS_SCHEMA)
        self.assertIsNone(packet["user_decision"])
        report = (Path(result["folder"]) / "score/llm_gate_report.md").read_text(
            encoding="utf-8"
        )
        self.assertTrue(
            all(
                word in report
                for word in ("Strengths", "Gaps", "Keywords", "Tailoring plan")
            )
        )
        self.assertFalse((Path(result["folder"]) / "generated").exists())
        payload = json.loads(self.requests[0]["messages"][1]["content"])
        self.assertEqual(payload["profile"], self.profile)
        self.assertNotIn("master_career_data.yaml", json.dumps(payload))

    def test_new_call_reports_provider_usage(self):
        result = self.run_job()
        self.assertEqual(
            result["usage"]["this_run"],
            {
                "provider_requests": 1,
                "prompt_tokens": 101,
                "completion_tokens": 29,
                "total_tokens": 130,
                "reasoning_tokens": 11,
                "actual_usd": 0.000123,
            },
        )
        self.assertEqual(
            result["usage"]["by_stage"]["tier1"]["source"], "new_provider_call"
        )
        self.assertEqual(result["cache"]["tier1"]["usage"]["actual_usd"], 0.000123)

    def test_openrouter_reasoning_effort_is_sent_as_extra_body(self):
        config = read_json(self.root / "config/model_profiles.local.json")
        config["profiles"]["quality"]["reasoning_effort"] = "low"
        write_json(self.root / "config/model_profiles.local.json", config)
        client = self.factory("quality")
        request = client.build_requests(
            [{"role": "user", "content": "Return a package."}],
            json_schema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        )[0]
        self.assertEqual(
            request.parameters["extra_body"],
            {"reasoning": {"effort": "low", "exclude": True}},
        )

    def test_missing_model_score_is_unavailable_not_zero(self):
        self.analysis.pop("score")
        result = self.run_job()
        self.assertIsNone(result["highlights"]["score"])
        report = (Path(result["folder"]) / "score/llm_gate_report.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Score: unavailable", report)

    def test_single_text_list_field_is_normalized(self):
        self.analysis["tailoring_plan"] = "Lead with relevant performance experience."
        result = self.run_job()
        packet = read_json(Path(result["folder"]) / "tailored/job_packet.json")
        self.assertEqual(
            packet["analysis"]["tailoring_plan"],
            ["Lead with relevant performance experience."],
        )

    def test_cover_body_text_is_normalized_to_paragraph_list(self):
        self.package["cover"]["body"] = self.package["cover"]["body"][0]
        result = self.run_job("generate", cover=True)
        self.assertEqual(result["state"], "READY_TO_APPLY")

    def test_generation_renders_real_docx_and_defaults_ready(self):
        result = self.run_job("generate", cover=True)
        self.assertEqual(result["state"], "READY_TO_APPLY")
        self.assertEqual(self.meta(result)["status"], "READY_TO_APPLY")
        self.assertEqual(
            [r["model"] for r in self.requests], ["test-economy", "test-quality"]
        )
        for name in ("resume", "cover"):
            text = "\n".join(p.text for p in Document(result[name]).paragraphs)
            self.assertIn(self.profile["identity"]["name"], text)
        self.assertFalse((Path(result["folder"]) / "application.json").exists())
        resume = read_json(
            Path(result["resume"]).parent / "resume_intermediate_v1.json"
        )
        self.assertEqual(resume["experience"][0]["company"], "LTIMindtree")
        self.assertEqual(
            resume["experience"][0]["title"], "Capacity & Performance Specialist"
        )
        self.assertEqual(resume["experience"][0]["start_date"], "")
        self.assertIn("not production", " ".join(resume["experience"][0]["bullets"]))
        self.assertEqual(self.meta(result)["user_decision"]["decision"], "ACCEPTED")
        self.assertIn("-Mode apply -AssumeApplied", result["next_command"])

    def test_suitability_override_recorded_and_continues(self):
        self.analysis["recommendation"] = "SKIP"
        first = self.run_job("generate")
        self.assertEqual(first["state"], "AWAITING_DECISION")
        self.assertEqual(len(self.requests), 1)
        result = self.run_job(
            "generate", override_suitability=True, reason="Strategic application"
        )
        decision = self.meta(result)["user_decision"]
        self.assertTrue(decision["suitability_override"])
        self.assertEqual(decision["reason"], "Strategic application")
        self.assertEqual(result["llm_decision"], "SKIP")
        self.assertEqual(result["state"], "READY_TO_APPLY")
        self.assertEqual(len(self.requests), 2)

    def test_real_cache_hits_skip_both_calls_and_renderer(self):
        first = self.run_job("generate", cover=True)
        before = Path(first["resume"]).read_bytes()
        with patch(
            "src.pipeline.artifacts.render_local",
            side_effect=AssertionError("Cached render must not rerun"),
        ):
            again = self.run_job("generate", cover=True)
        self.assertEqual(len(self.requests), 2)
        self.assertEqual([v["result"] for v in again["cache"].values()], ["HIT", "HIT"])
        self.assertEqual(before, Path(again["resume"]).read_bytes())
        self.assertEqual(again["cost"]["max_new_provider_requests"], 0)

    def test_model_switch_invalidates_cache_and_records_model(self):
        first = self.run_job()
        self.configure(economy="test-economy-new")
        second = self.run_job()
        self.assertNotEqual(
            first["cache"]["tier1"]["key"], second["cache"]["tier1"]["key"]
        )
        self.assertEqual(len(self.requests), 2)
        self.assertEqual(
            second["cache"]["tier1"]["model_used"]["model"], "test-economy-new"
        )

    def test_named_profiles_are_selected_per_stage(self):
        config = read_json(self.root / "config/model_profiles.local.json")
        config["profiles"].update(
            {
                "economy_deepseek": {
                    "primary": {
                        "provider": "openrouter",
                        "model": "test-deepseek",
                        "supports_json_schema": True,
                    },
                    "fallbacks": [],
                },
                "quality_claude": {
                    "primary": {
                        "provider": "openrouter",
                        "model": "test-claude",
                        "supports_json_schema": True,
                    },
                    "fallbacks": [],
                    "allow_artifacts": True,
                },
            }
        )
        write_json(self.root / "config/model_profiles.local.json", config)
        result = self.run_job(
            "generate",
            analysis_profile="economy_deepseek",
            generation_profile="quality_claude",
        )
        self.assertEqual(result["state"], "READY_TO_APPLY")
        self.assertEqual(
            result["profiles"],
            {"analysis": "economy_deepseek", "generation": "quality_claude"},
        )
        self.assertEqual(
            [request["model"] for request in self.requests],
            ["test-deepseek", "test-claude"],
        )

    def test_named_generation_profile_requires_artifact_policy(self):
        config = read_json(self.root / "config/model_profiles.local.json")
        config["profiles"]["quality_claude"] = {
            "primary": {
                "provider": "openrouter",
                "model": "test-claude",
                "supports_json_schema": True,
            },
            "fallbacks": [],
            "allow_artifacts": False,
        }
        write_json(self.root / "config/model_profiles.local.json", config)
        with self.assertRaises(PipelineError):
            self.run_job("generate", generation_profile="quality_claude")
        self.assertEqual(len(self.requests), 1)

    def test_request_changes_invalidate_cache(self):
        first = self.run_job()
        with patch(
            "scripts.canonical_runner.ANALYSIS_PROMPT", "Changed analysis prompt"
        ):
            second = self.run_job()
        self.assertNotEqual(
            first["cache"]["tier1"]["key"], second["cache"]["tier1"]["key"]
        )

    def test_apply_only_changes_only_target_and_is_idempotent(self):
        old = self.historical_job(
            "Different historical position in another business entirely with unrelated duties."
        )
        before = (old / "metadata.yaml").read_bytes()
        result = self.run_job("generate", cover=True)
        resume_before = Path(result["resume"]).read_bytes()
        args = dict(
            assume_applied=True,
            method="Indeed",
            applied_date="2026-09-12",
            notes="Submitted manually",
        )
        with patch(
            "scripts.canonical_runner.stage_call",
            side_effect=AssertionError("Apply cannot call a model"),
        ):
            applied = self.run_job("apply", **args)
            repeated = self.run_job("apply", **args)
        self.assertEqual(applied["state"], "ASSUMED_APPLIED")
        self.assertEqual(len(self.meta(repeated)["application"]["history"]), 1)
        self.assertEqual(before, (old / "metadata.yaml").read_bytes())
        self.assertEqual(resume_before, Path(result["resume"]).read_bytes())
        self.assertEqual(len(self.requests), 2)
        gate = self.run_job("gate")
        self.assertEqual(gate["state"], "BLOCKED")
        self.assertEqual(self.meta(gate)["status"], "ASSUMED_APPLIED")

    def test_generate_assume_applied_flag_records_application(self):
        result = self.run_job(
            "generate", assume_applied=True, method="Indeed", applied_date="2026-09-12"
        )
        self.assertEqual(result["state"], "ASSUMED_APPLIED")
        self.assertTrue(self.meta(result)["application"]["applied"])

    def test_apply_rejects_missing_flag_or_invalid_dates_without_calls(self):
        for args in (
            {},
            {"assume_applied": True, "method": "Indeed", "applied_date": "2026-02-30"},
            {"assume_applied": True, "method": " ", "applied_date": "2026-09-12"},
        ):
            with self.assertRaises(PipelineError):
                self.run_job("apply", **args)
        self.assertEqual(self.requests, [])
        self.assertFalse((self.root / "data/jobs").exists())

    def test_failed_call_can_retry_after_fix(self):
        self.status = 500
        with self.assertRaises(PipelineError):
            self.run_job()
        self.assertEqual(len(self.requests), 1)
        self.status = 200
        result = self.run_job()
        self.assertEqual(result["state"], "TRIAGED")
        self.assertEqual(len(self.requests), 2)

    def test_invalid_analysis_and_client_leak_fail_before_package(self):
        self.analysis["fit_rationale"] = "Bank of America"
        with self.assertRaises(PipelineError):
            self.run_job("generate")
        self.assertEqual(len(self.requests), 1)

    def test_invalid_package_fails_before_render(self):
        self.package["resume"]["experience"][0]["bullet_ids"] = ["citi_etl"]
        with patch(
            "src.pipeline.artifacts.render_local",
            side_effect=AssertionError("Invalid package cannot render"),
        ):
            with self.assertRaises(PipelineError):
                self.run_job("generate")
        self.assertEqual(len(self.requests), 2)

    def test_runtime_tampering_blocks_before_provider(self):
        (self.root / PROFILE_PATH).write_text("{}", encoding="utf-8")
        with self.assertRaises(PipelineError):
            self.run_job()
        self.assertEqual(self.requests, [])

    def test_fallback_and_artifact_policy_are_enforced(self):
        self.configure(fallback=True)
        with self.assertRaises(PipelineError):
            self.run_job()
        self.assertEqual(self.requests, [])
        self.configure(artifacts=False)
        with self.assertRaises(PipelineError):
            self.run_job("generate")
        self.assertEqual(len(self.requests), 1)

    def test_generated_edits_preserved_and_apply_blocked(self):
        result = self.run_job("generate")
        path = Path(result["resume"])
        path.write_bytes(b"manual edit kept")
        with self.assertRaises(PipelineError):
            self.run_job("generate")
        with self.assertRaises(PipelineError):
            self.run_job(
                "apply", assume_applied=True, method="Indeed", applied_date="2026-09-12"
            )
        self.assertEqual(path.read_bytes(), b"manual edit kept")
        self.assertEqual(len(self.requests), 2)

    def test_cover_toggle_keeps_previous_package(self):
        first = self.run_job("generate", cover=True)
        second = self.run_job("generate")
        self.assertIsNone(second["cover"])
        self.assertTrue(Path(first["cover"]).exists())
        self.assertNotEqual(Path(first["resume"]).parent, Path(second["resume"]).parent)
        self.assertEqual(len(self.requests), 3)

    def test_folder_collision_and_lock_do_not_overwrite(self):
        folder = self.root / "data/jobs" / ("runner_" + job_hash(JOB)[:8])
        folder.mkdir(parents=True)
        marker = folder / "metadata.yaml"
        marker.write_text("job_hash: other\ncanonical_runner: true\n", encoding="utf-8")
        before = marker.read_bytes()
        with self.assertRaises(PipelineError):
            self.run_job()
        self.assertEqual(marker.read_bytes(), before)
        with workspace_lock(self.root):
            with self.assertRaises(PipelineError):
                self.run_job()
        self.assertEqual(self.requests, [])

    def test_cli_dry_run_without_profile_or_models_never_calls_provider(self):
        self.historical_job()
        (self.root / PROFILE_PATH).unlink()
        result = subprocess.run(
            [
                sys.executable,
                str(REPO / "scripts/canonical_runner.py"),
                str(self.intake),
                "--root",
                str(self.root),
                "--dry-run",
                "--json",
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["state"], "BLOCKED")
        self.assertEqual(output["cost"]["max_new_provider_requests"], 0)

    def test_actual_faiss_search_with_synthetic_local_embedding(self):
        import faiss
        import numpy as np
        from scripts.utils import vector_ops

        index = faiss.IndexFlatIP(3)
        index.add(np.array([[1, 0, 0]], dtype="float32"))
        with patch.object(
            vector_ops,
            "load_index_and_metadata",
            return_value=(index, [{"uuid": "old-job"}]),
        ), patch.object(
            vector_ops,
            "get_embedding",
            return_value=np.array([[1, 0, 0]], dtype="float32"),
        ):
            result = semantic_worker(self.root, JOB, "different-job")
        self.assertEqual(result["status"], "DUPLICATE")
        self.assertEqual(result["matches"][0]["similarity"], 1.0)

    def test_whitespace_only_intake_reuses_paid_cache(self):
        first = self.run_job()
        self.assertEqual(first["cache"]["tier1"]["result"], "MISS")
        self.intake.write_text(
            "  \n" + JOB.replace(" ", "  ") + "\n\n", encoding="utf-8"
        )
        second = self.run_job()
        self.assertEqual(
            paid_job_text("  \n" + JOB.replace(" ", "  ") + "\n\n"), paid_job_text(JOB)
        )
        self.assertEqual(second["folder"], first["folder"])
        self.assertEqual(second["cache"]["tier1"]["result"], "HIT")
        self.assertEqual(
            second["cache"]["tier1"]["key"], first["cache"]["tier1"]["key"]
        )
        self.assertEqual(len(self.requests), 1)

    def test_failed_rerun_replaces_stale_success_handoff(self):
        first = self.run_job()
        handoff = Path(first["folder"]) / "runner_result.json"
        self.assertEqual(read_json(handoff)["state"], "TRIAGED")
        self.status = 500
        with self.assertRaises(PipelineError):
            self.run_job("generate")
        current = read_json(handoff)
        self.assertEqual(current["state"], "FAILED")
        self.assertIsNone(current["resume"])
        self.assertIsNone(current["next_command"])
        self.assertEqual(self.meta(first)["last_runner_state"], "FAILED")
        self.assertEqual(self.meta(first)["status"], "FAILED")

    def test_continuation_keeps_one_reason_and_cover(self):
        self.analysis["recommendation"] = "SKIP"
        self.historical_job()
        result = self.run_job(
            "generate",
            override_duplicate=True,
            reason="Verified distinct requisition",
            cover=True,
        )
        self.assertEqual(result["state"], "AWAITING_DECISION")
        command = result["next_command"]
        self.assertEqual(command.count("-Reason"), 1)
        self.assertIn("-Cover", command)
        self.assertIn("-OverrideDuplicate", command)
        self.assertIn("-OverrideSuitability", command)
        self.assertIn("-Mode generate", command)
        self.assertIn("Verified distinct requisition", command)
        self.assertNotIn("-Reason '<actual authorized reason>'", command)


if __name__ == "__main__":
    unittest.main()
